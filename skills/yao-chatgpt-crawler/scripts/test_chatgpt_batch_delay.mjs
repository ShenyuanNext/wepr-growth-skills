#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(__filename);
const skillRoot = path.resolve(scriptDir, '..');
const batchScript = path.join(scriptDir, 'chatgpt_batch_crawl.mjs');

function run(args, options = {}) {
  return spawnSync(process.execPath, [batchScript, ...args], {
    cwd: skillRoot,
    encoding: 'utf8',
    ...options,
  });
}

function dryRun(root, name, extraArgs = []) {
  const outDir = path.join(root, name);
  const result = run([
    '--questions',
    path.join(root, 'questions.txt'),
    '--repeat',
    '1',
    '--target-entity',
    '豆包',
    '--entity-type',
    'product',
    '--dry-run',
    '--out-dir',
    outDir,
    ...extraArgs,
  ]);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(fs.readFileSync(path.join(outDir, 'chatgpt-crawl.json'), 'utf8')).input.delay_strategy;
}

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'yao-chatgpt-delay-'));
fs.writeFileSync(path.join(root, 'questions.txt'), '国产大模型有哪些？\n', 'utf8');

assert.deepEqual(dryRun(root, 'default'), {
  mode: 'random',
  preset: 'default_30s_1m',
  label: '30s-1m',
  min_ms: 30000,
  max_ms: 60000,
  min_minutes: 0.5,
  max_minutes: 1,
});

assert.deepEqual(dryRun(root, 'balanced', ['--delay-preset', '1-3m']), {
  mode: 'random',
  preset: 'balanced_1_3m',
  label: '1-3m',
  min_ms: 60000,
  max_ms: 180000,
  min_minutes: 1,
  max_minutes: 3,
});

assert.deepEqual(dryRun(root, 'safe', ['--safe-random-delay']), {
  mode: 'random',
  preset: 'conservative_3_10m',
  label: '3-10m',
  min_ms: 180000,
  max_ms: 600000,
  min_minutes: 3,
  max_minutes: 10,
});

assert.deepEqual(dryRun(root, 'custom', ['--delay-min-minutes', '5', '--delay-max-minutes', '20']), {
  mode: 'random',
  preset: 'custom',
  label: '5m-20m',
  min_ms: 300000,
  max_ms: 1200000,
  min_minutes: 5,
  max_minutes: 20,
});

assert.deepEqual(dryRun(root, 'fixed', ['--delay-ms', '1500']), {
  mode: 'fixed',
  delay_ms: 1500,
  delay_minutes: 0.025,
});

const missingMin = run([
  '--questions',
  path.join(root, 'questions.txt'),
  '--delay-max-minutes',
  '3',
  '--dry-run',
]);
assert.notEqual(missingMin.status, 0, 'custom random max without min should fail');
assert.match(missingMin.stderr, /Random delay requires both a minimum and a maximum/);

fs.rmSync(root, { recursive: true, force: true });
console.log('chatgpt batch delay regression: PASS');
