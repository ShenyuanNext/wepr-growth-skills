#!/usr/bin/env node
import { execFileSync, spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const OPENCLI_REPO = 'jackwener/opencli';
const DEFAULT_URL = 'https://chat.deepseek.com/';
const DEFAULT_DEBUG_PORT = 9230;
const home = os.homedir();
const extensionRoot = path.join(home, '.opencli', 'extensions');
const browserCandidates = {
  edge: {
    name: 'Microsoft Edge',
    path: '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    profileDir: path.join(home, '.opencli', 'edge-deepseek-profile'),
  },
  chrome: {
    name: 'Google Chrome',
    path: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    profileDir: path.join(home, '.opencli', 'chrome-deepseek-profile'),
  },
};

function printHelp() {
  console.log(`Usage:
  node scripts/setup_deepseek_bridge.mjs [options]

Options:
  --browser <edge|chrome>     Browser to launch. Default: first installed browser.
  --url <url>                 Page to open after Bridge loads. Default: ${DEFAULT_URL}
  --profile-dir <dir>         Browser user-data-dir. Default: ~/.opencli/<browser>-deepseek-profile
  --debug-port <port>         Remote debugging port. Default: ${DEFAULT_DEBUG_PORT}
  --no-daemon-restart         Do not restart the OpenCLI daemon first.
  --dry-run                   Print the launch plan without opening a browser.
  -h, --help                  Show help.
`);
}

function parseArgs(argv) {
  const args = {
    browser: '',
    url: DEFAULT_URL,
    profileDir: '',
    debugPort: DEFAULT_DEBUG_PORT,
    restartDaemon: true,
    dryRun: false,
    help: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--browser') args.browser = takeArgValue(argv, ++i, arg);
    else if (arg === '--url') args.url = takeArgValue(argv, ++i, arg);
    else if (arg === '--profile-dir') args.profileDir = path.resolve(takeArgValue(argv, ++i, arg));
    else if (arg === '--debug-port') args.debugPort = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--no-daemon-restart') args.restartDaemon = false;
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!Number.isInteger(args.debugPort) || args.debugPort < 1024 || args.debugPort > 65535) {
    throw new Error('--debug-port must be an integer between 1024 and 65535');
  }
  if (!isAllowedDeepSeekUrl(args.url)) {
    throw new Error('--url must point to https://chat.deepseek.com/ for this skill setup');
  }
  return args;
}

function takeArgValue(argv, index, flag) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`${flag} requires a value`);
  }
  return value;
}

function isAllowedDeepSeekUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && url.hostname === 'chat.deepseek.com';
  } catch {
    return false;
  }
}

function run(cmd, args, options = {}) {
  return execFileSync(cmd, args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    ...options,
  }).trim();
}

function safeRun(cmd, args) {
  try {
    return run(cmd, args);
  } catch (error) {
    return `${error.stdout ?? ''}${error.stderr ?? ''}`.trim();
  }
}

function currentOpenCliVersion() {
  return run('opencli', ['--version']);
}

function chooseBrowser(name) {
  if (name) {
    const browser = browserCandidates[name];
    if (!browser) throw new Error(`Unsupported browser: ${name}. Use edge or chrome.`);
    if (!fs.existsSync(browser.path)) throw new Error(`${browser.name} not found at ${browser.path}`);
    return browser;
  }
  for (const browser of Object.values(browserCandidates)) {
    if (fs.existsSync(browser.path)) return browser;
  }
  throw new Error('Neither Microsoft Edge nor Google Chrome was found in /Applications.');
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'yao-deepseek-crawler-setup',
    },
  });
  if (!response.ok) {
    throw new Error(`GitHub API failed: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

async function downloadFile(url, targetPath, tagName, assetName) {
  try {
    const response = await fetch(url, {
      headers: { 'User-Agent': 'yao-deepseek-crawler-setup' },
    });
    if (!response.ok) {
      throw new Error(`Download failed: ${response.status} ${await response.text()}`);
    }
    fs.writeFileSync(targetPath, Buffer.from(await response.arrayBuffer()));
    return;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.log(`Node download failed (${message}); trying curl...`);
  }

  try {
    run('curl', ['-L', '--fail', '--silent', '--show-error', '-o', targetPath, url]);
    return;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.log(`curl download failed (${message}); trying gh release download...`);
  }

  fs.rmSync(targetPath, { force: true });
  run('gh', ['release', 'download', tagName, '-R', OPENCLI_REPO, '-p', assetName, '--dir', path.dirname(targetPath), '--clobber']);
}

function findManifestDir(root) {
  const stack = [root];
  while (stack.length) {
    const current = stack.pop();
    const manifest = path.join(current, 'manifest.json');
    if (fs.existsSync(manifest)) return current;
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      if (entry.isDirectory()) stack.push(path.join(current, entry.name));
    }
  }
  return null;
}

function patchExtensionHost(manifestDir) {
  const backgroundPath = path.join(manifestDir, 'dist', 'background.js');
  if (!fs.existsSync(backgroundPath)) return false;
  const original = fs.readFileSync(backgroundPath, 'utf8');
  const patched = original.replace('const DAEMON_HOST = "localhost";', 'const DAEMON_HOST = "127.0.0.1";');
  if (patched === original) return false;
  fs.writeFileSync(backgroundPath, patched);
  return true;
}

async function ensureExtension() {
  fs.mkdirSync(extensionRoot, { recursive: true });
  const opencliVersion = currentOpenCliVersion();
  const tagName = `v${opencliVersion}`;
  const release = await fetchJson(`https://api.github.com/repos/${OPENCLI_REPO}/releases/tags/${tagName}`);
  const asset = (release.assets ?? []).find((item) => /extension.*\.zip$/i.test(item.name));
  if (!asset) {
    throw new Error(`No extension zip found on ${release.html_url}`);
  }

  const assetBase = asset.name.replace(/\.zip$/i, '');
  const targetDir = path.join(extensionRoot, assetBase);
  const manifestDir = fs.existsSync(targetDir) ? findManifestDir(targetDir) : null;
  if (manifestDir) {
    patchExtensionHost(manifestDir);
    return { manifestDir, assetName: asset.name, reused: true };
  }

  const zipPath = path.join(extensionRoot, asset.name);
  console.log(`Downloading ${asset.name}...`);
  await downloadFile(asset.browser_download_url, zipPath, tagName, asset.name);

  fs.rmSync(targetDir, { recursive: true, force: true });
  fs.mkdirSync(targetDir, { recursive: true });
  run('unzip', ['-q', '-o', zipPath, '-d', targetDir]);

  const unpackedManifestDir = findManifestDir(targetDir);
  if (!unpackedManifestDir) {
    throw new Error(`Extension manifest.json not found after unpacking ${asset.name}`);
  }
  patchExtensionHost(unpackedManifestDir);
  return { manifestDir: unpackedManifestDir, assetName: asset.name, reused: false };
}

function stopExistingProfile(profileDir) {
  try {
    run('pkill', ['-f', profileDir]);
  } catch {
  }
}

function launchBrowser({ browser, extensionDir, profileDir, debugPort, url }) {
  fs.mkdirSync(profileDir, { recursive: true });
  stopExistingProfile(profileDir);
  const args = [
    `--user-data-dir=${profileDir}`,
    `--load-extension=${extensionDir}`,
    `--disable-extensions-except=${extensionDir}`,
    `--remote-debugging-port=${debugPort}`,
    '--no-first-run',
    '--new-window',
    url,
  ];
  const child = spawn(browser.path, args, {
    detached: true,
    stdio: 'ignore',
  });
  child.unref();
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const browser = chooseBrowser(options.browser);
  const profileDir = options.profileDir || browser.profileDir;

  if (options.dryRun) {
    console.log(JSON.stringify({
      ok: true,
      dry_run: true,
      browser: browser.name,
      browser_path: browser.path,
      profile_dir: profileDir,
      url: options.url,
      debug_port: options.debugPort,
      opens_deepseek_only: true,
    }, null, 2));
    return;
  }

  console.log(`opencli ${currentOpenCliVersion()}`);
  if (options.restartDaemon) {
    console.log(safeRun('opencli', ['daemon', 'restart']));
  }

  const extension = await ensureExtension();
  console.log(`${extension.reused ? 'Using' : 'Installed'} ${extension.assetName}`);
  console.log(`Extension path: ${extension.manifestDir}`);
  console.log(`${browser.name} profile: ${profileDir}`);
  console.log(`Opening: ${options.url}`);

  launchBrowser({
    browser,
    extensionDir: extension.manifestDir,
    profileDir,
    debugPort: options.debugPort,
    url: options.url,
  });
  console.log(`${browser.name} launched. Waiting for Browser Bridge...`);

  await new Promise((resolve) => setTimeout(resolve, 5000));
  console.log('\n=== opencli doctor ===');
  console.log(safeRun('opencli', ['doctor']));
  console.log('\n=== opencli profile list ===');
  console.log(safeRun('opencli', ['profile', 'list']));
  console.log(`\nIf DeepSeek asks for login, finish login in the opened ${browser.name} window and rerun \`opencli deepseek whoami -f json\`.`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
