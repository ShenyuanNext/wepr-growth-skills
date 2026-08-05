#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const EXCLUDED_REFERENCE_DOMAINS = new Set(['chatgpt.com', 'chat.openai.com']);

function parseArgs(argv) {
  const args = {
    timeout: 300,
    search: true,
    deepResearch: false,
    model: '',
    profile: '',
    siteSession: 'persistent',
    newConversation: true,
    browserSession: '',
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--prompt' || arg === '-p') args.prompt = argv[++i];
    else if (arg === '--profile') args.profile = argv[++i];
    else if (arg === '--timeout') args.timeout = Number(argv[++i]);
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--target') args.target = argv[++i];
    else if (arg === '--model') args.model = argv[++i];
    else if (arg === '--conversation') args.conversation = argv[++i];
    else if (arg === '--site-session') args.siteSession = argv[++i];
    else if (arg === '--browser-session') args.browserSession = argv[++i];
    else if (arg === '--session') args.session = argv[++i];
    else if (arg === '--no-search') args.search = false;
    else if (arg === '--deep-research') args.deepResearch = true;
    else if (arg === '--no-new') args.newConversation = false;
    else if (arg === '--capture-current') args.captureCurrent = true;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else if (!args.prompt) args.prompt = arg;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/chatgpt_browser_crawl.mjs --profile <profile> --prompt <question> [options]

Options:
  --profile <name>        OpenCLI Browser Bridge profile alias/id.
  --timeout <seconds>     Max seconds to wait. Default: 300.
  --target <text>         Optional target term to count in the answer.
  --model <mode>          Optional ChatGPT mode: instant, thinking, or pro.
  --conversation <id>     Continue an existing conversation instead of starting fresh.
  --site-session <mode>   OpenCLI site session: persistent or ephemeral. Default: persistent.
  --browser-session <id>  Browser Bridge session for DOM source extraction.
  --no-search             Do not request ChatGPT Web Search.
  --deep-research         Request ChatGPT Deep Research instead of a normal web-search answer.
  --no-new                Do not pass --new to opencli chatgpt ask.
  --capture-current       Capture the current ChatGPT conversation instead of sending.
  --out <file>            Save normalized JSON.
  -h, --help              Show help.
`);
}

function validateOptions(options) {
  if (options.help) return;
  if (!options.captureCurrent && !options.prompt) throw new Error('Missing --prompt <question>');
  if (!Number.isInteger(options.timeout) || options.timeout < 30 || options.timeout > 7200) {
    throw new Error('--timeout must be an integer between 30 and 7200');
  }
  if (options.model && !['instant', 'thinking', 'pro'].includes(options.model)) {
    throw new Error('--model must be one of: instant, thinking, pro');
  }
  if (!['persistent', 'ephemeral'].includes(options.siteSession)) {
    throw new Error('--site-session must be persistent or ephemeral');
  }
}

function runOpenCli(args, options = {}) {
  const fullArgs = [];
  if (options.profile) fullArgs.push('--profile', options.profile);
  fullArgs.push(...args);
  try {
    return execFileSync('opencli', fullArgs, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: options.timeoutMs ?? 360000,
      maxBuffer: 20 * 1024 * 1024,
    });
  } catch (error) {
    const output = `${error.stdout ?? ''}${error.stderr ?? ''}`.trim();
    throw new Error(output || error.message);
  }
}

function parseJsonFromOpenCli(output) {
  const trimmed = String(output || '').trim();
  try {
    return JSON.parse(trimmed);
  } catch {}
  const arrayStart = trimmed.indexOf('[');
  const objectStart = trimmed.indexOf('{');
  const starts = [arrayStart, objectStart].filter((index) => index >= 0);
  if (!starts.length) throw new Error(`No JSON found in opencli output:\n${trimmed}`);
  const start = Math.min(...starts);
  const lastArray = trimmed.lastIndexOf(']');
  const lastObject = trimmed.lastIndexOf('}');
  const end = Math.max(lastArray, lastObject);
  if (end < start) throw new Error(`Malformed JSON in opencli output:\n${trimmed}`);
  return JSON.parse(trimmed.slice(start, end + 1));
}

function cleanText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function multilineText(value) {
  return String(value || '').replace(/\r\n/g, '\n').trim();
}

function compactOutput(value, maxLength = 5000) {
  const text = multilineText(value);
  return text.length <= maxLength ? text : `${text.slice(0, maxLength)}...`;
}

function firstRecord(value) {
  if (Array.isArray(value)) return firstRecord(value[0]);
  if (!value || typeof value !== 'object') return value;
  for (const key of ['data', 'rows', 'result', 'results']) {
    if (Array.isArray(value[key]) && value[key].length) return firstRecord(value[key][0]);
    if (value[key] && typeof value[key] === 'object') return firstRecord(value[key]);
  }
  return value;
}

function findStringByKeys(value, keys) {
  if (!value) return '';
  if (typeof value === 'string') return '';
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findStringByKeys(item, keys);
      if (found) return found;
    }
    return '';
  }
  if (typeof value !== 'object') return '';
  for (const key of keys) {
    if (typeof value[key] === 'string' && cleanText(value[key])) return multilineText(value[key]);
  }
  for (const child of Object.values(value)) {
    const found = findStringByKeys(child, keys);
    if (found) return found;
  }
  return '';
}

function directText(value) {
  if (!value || typeof value !== 'object') return '';
  for (const key of ['response', 'answer', 'assistant', 'content', 'Text', 'text']) {
    if (typeof value[key] === 'string' && cleanText(value[key])) return multilineText(value[key]);
  }
  return '';
}

function extractAssistantMessage(value) {
  if (!value) return '';
  if (Array.isArray(value)) {
    for (let i = value.length - 1; i >= 0; i -= 1) {
      const found = extractAssistantMessage(value[i]);
      if (found) return found;
    }
    return '';
  }
  if (typeof value !== 'object') return '';
  const role = cleanText(value.role || value.Role || value.author || value.Author).toLowerCase();
  if (role.includes('assistant')) {
    const text = directText(value);
    if (text) return text;
  }
  for (const key of ['messages', 'rows', 'data', 'result', 'results']) {
    if (value[key]) {
      const found = extractAssistantMessage(value[key]);
      if (found) return found;
    }
  }
  return '';
}

function extractUserMessage(value) {
  if (!value) return '';
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = extractUserMessage(item);
      if (found) return found;
    }
    return '';
  }
  if (typeof value !== 'object') return '';
  const role = cleanText(value.role || value.Role || value.author || value.Author).toLowerCase();
  if (role.includes('user')) {
    const text = directText(value);
    if (text) return text;
  }
  for (const key of ['messages', 'rows', 'data', 'result', 'results']) {
    if (value[key]) {
      const found = extractUserMessage(value[key]);
      if (found) return found;
    }
  }
  return '';
}

function extractAnswerText(parsed) {
  const assistantMessage = extractAssistantMessage(parsed);
  if (assistantMessage) return assistantMessage;
  const record = firstRecord(parsed);
  const direct = findStringByKeys(record, ['response', 'answer', 'assistant', 'content', 'Text', 'text']);
  if (direct) return direct;
  if (typeof record === 'string') return multilineText(record);
  return '';
}

function extractConversation(parsed) {
  const record = firstRecord(parsed);
  return {
    id: findStringByKeys(record, ['conversationId', 'conversation_id', 'id']),
    url: findStringByKeys(record, ['conversationUrl', 'conversation_url', 'url']),
    tool: findStringByKeys(record, ['tool']),
  };
}

function extractHeadings(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => /^#{1,6}\s+\S/.test(line))
    .map((line) => line.replace(/^#{1,6}\s+/, ''));
}

function countOccurrences(text, target) {
  if (!target) return null;
  const escaped = target.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = text.match(new RegExp(escaped, 'gi'));
  return matches ? matches.length : 0;
}

function domainFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '').toLowerCase();
  } catch {
    return '';
  }
}

function stripTrailingPunctuation(url) {
  return String(url || '').replace(/[),\].。；;，、,.]+$/g, '');
}

function isExcludedReferenceUrl(url, domain = domainFromUrl(url)) {
  if (EXCLUDED_REFERENCE_DOMAINS.has(domain)) return true;
  try {
    const parsed = new URL(url);
    const hostname = parsed.hostname.replace(/^www\./, '').toLowerCase();
    if (hostname === 'google.com' && parsed.pathname === '/s2/favicons') return true;
    if (hostname === 'icons.duckduckgo.com') return true;
  } catch {}
  return false;
}

function referenceKey(url) {
  try {
    const parsed = new URL(stripTrailingPunctuation(url));
    parsed.hash = '';
    for (const key of [...parsed.searchParams.keys()]) {
      if (/^(utm_|fbclid$|gclid$|mc_)/i.test(key)) parsed.searchParams.delete(key);
    }
    return parsed.toString().replace(/\/$/, '').toLowerCase();
  } catch {
    return stripTrailingPunctuation(url).replace(/\/$/, '').toLowerCase();
  }
}

function cleanReferenceItem(ref, fallbackPosition = 'answer_text') {
  const cleanedUrl = stripTrailingPunctuation(ref?.url);
  const domain = domainFromUrl(cleanedUrl || '');
  if (!cleanedUrl || !domain) return null;
  if (isExcludedReferenceUrl(cleanedUrl, domain)) return null;
  const positions = Array.isArray(ref.positions) ? ref.positions : [ref.source_position || ref.position || fallbackPosition];
  const uniquePositions = [...new Set(positions.map(cleanText).filter(Boolean))];
  const sourcePosition = uniquePositions.join('+') || fallbackPosition;
  return {
    number: Number.isFinite(Number(ref.number)) ? Number(ref.number) : null,
    source: cleanText(ref.source) || domain,
    domain,
    title: cleanText(ref.title) || cleanText(ref.source) || domain,
    date: cleanText(ref.date),
    url: cleanedUrl,
    summary: cleanText(ref.summary),
    source_position: sourcePosition,
    positions: uniquePositions.length ? uniquePositions : [fallbackPosition],
    extraction_method: cleanText(ref.extraction_method) || fallbackPosition,
  };
}

function isWeakReferenceTitle(title, domain) {
  const cleaned = cleanText(title).toLowerCase();
  return !cleaned || cleaned === domain || cleaned === `www.${domain}`;
}

function mergeReferenceCollections(collections, requested) {
  const merged = [];
  const byKey = new Map();
  const notes = [];
  const locationCounts = {};

  const addItem = (item, fallbackPosition) => {
    const ref = cleanReferenceItem(item, fallbackPosition);
    if (!ref) return;
    for (const position of ref.positions) {
      locationCounts[position] = (locationCounts[position] || 0) + 1;
    }
    const key = referenceKey(ref.url);
    const existing = byKey.get(key);
    if (!existing) {
      merged.push(ref);
      byKey.set(key, ref);
      return;
    }

    existing.positions = [...new Set([...existing.positions, ...ref.positions])];
    existing.source_position = existing.positions.join('+');
    existing.extraction_method = [...new Set([
      ...String(existing.extraction_method || '').split('+').filter(Boolean),
      ...String(ref.extraction_method || '').split('+').filter(Boolean),
    ])].join('+');

    if (isWeakReferenceTitle(existing.title, existing.domain) && !isWeakReferenceTitle(ref.title, ref.domain)) {
      existing.title = ref.title;
    } else if (ref.title.length > existing.title.length && ref.positions.includes('source_flyout')) {
      existing.title = ref.title;
    }
    if (!existing.date && ref.date) existing.date = ref.date;
    if (!existing.summary && ref.summary) existing.summary = ref.summary;
    if ((!existing.source || existing.source === existing.domain) && ref.source) existing.source = ref.source;
  };

  for (const collection of collections.filter(Boolean)) {
    if (collection.note) notes.push(collection.note);
    for (const item of collection.items || []) {
      addItem(item, item.source_position || item.position || collection.position || 'answer_text');
    }
  }

  merged.forEach((item, index) => {
    item.number = index + 1;
  });

  return {
    requested: Boolean(requested),
    count: merged.length,
    items: merged,
    locations: locationCounts,
    note: merged.length ? notes.filter(Boolean).join(' ') : (notes.filter(Boolean).join(' ') || 'No external URLs were found in the ChatGPT answer text or visible ChatGPT source controls.'),
  };
}

function collectReferencesFromText(text) {
  const items = [];
  const seen = new Set();

  const add = (title, url) => {
    const cleanedUrl = stripTrailingPunctuation(url);
    const domain = domainFromUrl(cleanedUrl);
    if (!cleanedUrl || !domain || isExcludedReferenceUrl(cleanedUrl, domain)) return;
    const key = cleanedUrl.toLowerCase();
    if (seen.has(key)) return;
    seen.add(key);
    items.push({
      number: items.length + 1,
      source: domain,
      domain,
      title: cleanText(title) || domain,
      date: '',
      url: cleanedUrl,
      summary: '',
      source_position: 'answer_text',
      positions: ['answer_text'],
      extraction_method: 'answer_text',
    });
  };

  const markdownLink = /\[([^\]\n]{1,220})\]\((https?:\/\/[^)\s]+)\)/g;
  for (const match of text.matchAll(markdownLink)) add(match[1], match[2]);

  const bareUrl = /https?:\/\/[^\s<>"')\]]+/g;
  for (const match of text.matchAll(bareUrl)) add('', match[0]);

  return {
    requested: true,
    count: items.length,
    items,
    note: items.length ? '' : 'No external URLs were found in the ChatGPT answer text.',
  };
}

function safeId(value, fallback = 'chatgpt-crawl') {
  const cleaned = String(value || '').trim().replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
  return (cleaned || fallback).slice(0, 80);
}

function conversationIdFromUrl(url) {
  const match = String(url || '').match(/\/c\/([^/?#]+)/);
  return match ? match[1] : '';
}

function extractStatusUrl(parsed) {
  const record = firstRecord(parsed);
  return findStringByKeys(record, ['Url', 'url', 'conversationUrl', 'conversation_url']);
}

function getChatGptStatus(options) {
  const output = runOpenCli(
    ['chatgpt', 'status', '-f', 'json', '--window', 'foreground', '--keep-tab', 'true'],
    { profile: options.profile, timeoutMs: 60000 },
  );
  const parsed = parseJsonFromOpenCli(output);
  return {
    parsed,
    output,
    url: extractStatusUrl(parsed),
  };
}

function shouldRetryWithoutExplicitWebSearch(error) {
  const message = error instanceof Error ? error.message : String(error || '');
  return /Could not find the ChatGPT Web Search tool option/i.test(message)
    || /ChatGPT did not create a conversation URL after sending the message/i.test(message);
}

const DOM_REFERENCE_EVAL = String.raw`(async () => {
  const excludedDomains = new Set(['chatgpt.com', 'chat.openai.com']);
  const clean = (value) => String(value || '').replace(/\s+/g, ' ').trim();
  const lines = (value) => String(value || '').split(/\n+/).map(clean).filter(Boolean);
  const domainFromUrl = (value) => {
    try {
      return new URL(value).hostname.replace(/^www\./, '').toLowerCase();
    } catch {
      return '';
    }
  };
  const isExternal = (href) => {
    const domain = domainFromUrl(href);
    return Boolean(domain && !excludedDomains.has(domain));
  };
  const titleFromAnchor = (anchor, textLines, domain, position) => {
    const title = clean(anchor.getAttribute('title'));
    const aria = clean(anchor.getAttribute('aria-label'));
    if (title && title !== domain) return title;
    if (position === 'source_flyout' && textLines[1]) return textLines[1];
    if (aria && aria !== domain) return aria;
    const nonDomain = textLines.find((line) => line !== domain && !line.includes(domain));
    return nonDomain || textLines[0] || domain;
  };
  const dateFromLines = (textLines) => textLines.find((line) => /(20\d{2}|19\d{2}|年|月|日|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i.test(line)) || '';
  const itemFromAnchor = (anchor, position, index) => {
    const href = anchor.href || anchor.getAttribute('href') || '';
    if (!isExternal(href)) return null;
    const domain = domainFromUrl(href);
    const textLines = lines(anchor.innerText || anchor.textContent || anchor.getAttribute('aria-label') || '');
    const source = clean(textLines[0]) || domain;
    const title = titleFromAnchor(anchor, textLines, domain, position);
    const date = position === 'source_flyout' ? dateFromLines(textLines.slice(2)) : dateFromLines(textLines);
    return {
      index: index + 1,
      source,
      domain,
      title,
      date,
      url: href,
      summary: position === 'source_flyout' ? clean(textLines.slice(3).join(' ')) : '',
      source_position: position,
      positions: [position],
      extraction_method: 'chatgpt_dom',
      dom_text: textLines.join('\n'),
    };
  };
  const main = document.querySelector('main') || document.body;
  const assistantTurns = [...main.querySelectorAll('[data-message-author-role="assistant"], [data-testid^="conversation-turn-"]')]
    .filter((node) => clean(node.innerText || node.textContent));
  const scope = assistantTurns.at(-1) || main;
  const inlineAnchors = [...scope.querySelectorAll('a[href]')]
    .filter((anchor) => anchor.closest('[data-testid="webpage-citation-pill"]') || anchor.querySelector('[data-testid="webpage-citation-pill"]'));
  const inline = inlineAnchors.map((anchor, index) => itemFromAnchor(anchor, 'inline_citation', index)).filter(Boolean);

  const sourceButton = [...scope.querySelectorAll('button')]
    .filter((button) => /^(来源|Sources?)$/i.test(clean(button.getAttribute('aria-label')) || clean(button.innerText || button.textContent)))
    .at(-1)
    || [...document.querySelectorAll('button')]
      .filter((button) => /^(来源|Sources?)$/i.test(clean(button.getAttribute('aria-label')) || clean(button.innerText || button.textContent)))
      .at(-1);
  let flyout = document.querySelector('[data-testid="screen-threadFlyOut"]') || document.querySelector('section[aria-label="来源"], section[aria-label="Sources"]');
  if (!flyout && sourceButton) {
    sourceButton.click();
    await new Promise((resolve) => setTimeout(resolve, 900));
    flyout = document.querySelector('[data-testid="screen-threadFlyOut"]') || document.querySelector('section[aria-label="来源"], section[aria-label="Sources"]');
  }
  const sourceAnchors = flyout ? [...flyout.querySelectorAll('a[href]')] : [];
  const sourceFlyout = sourceAnchors.map((anchor, index) => itemFromAnchor(anchor, 'source_flyout', index)).filter(Boolean);
  return {
    page: { url: location.href, title: document.title },
    scope_text_excerpt: clean((scope.innerText || scope.textContent || '').slice(0, 500)),
    source_button_found: Boolean(sourceButton),
    source_flyout_found: Boolean(flyout),
    inline,
    source_flyout: sourceFlyout,
  };
})()`;

function collectReferencesFromDom(options, conversationUrl) {
  if (!conversationUrl || !/^https:\/\/chatgpt\.com\/c\//.test(conversationUrl)) {
    return {
      requested: true,
      count: 0,
      items: [],
      note: 'No ChatGPT conversation URL was available for DOM source extraction.',
      raw: null,
    };
  }

  const session = safeId(options.browserSession || `chatgpt-crawl-${options.profile || 'default'}`);
  runOpenCli(['browser', session, 'open', conversationUrl], {
    profile: options.profile,
    timeoutMs: 90000,
  });
  const output = runOpenCli(['browser', session, 'eval', DOM_REFERENCE_EVAL], {
    profile: options.profile,
    timeoutMs: 90000,
  });
  const parsed = parseJsonFromOpenCli(output);
  const items = [
    ...((parsed.inline || []).map((item) => ({ ...item, source_position: 'inline_citation', positions: ['inline_citation'] }))),
    ...((parsed.source_flyout || []).map((item) => ({ ...item, source_position: 'source_flyout', positions: ['source_flyout'] }))),
  ];
  const note = items.length
    ? ''
    : `No DOM source links found. inline=${parsed.inline?.length || 0}; source_flyout=${parsed.source_flyout?.length || 0}; source_button=${Boolean(parsed.source_button_found)}; flyout=${Boolean(parsed.source_flyout_found)}.`;
  return {
    requested: true,
    count: items.length,
    items,
    note,
    raw: parsed,
  };
}

function captureCurrent(options) {
  const conversationId = options.conversation ? conversationIdFromUrl(options.conversation) || options.conversation : '';
  const readArgs = conversationId ? [
    'chatgpt',
    'detail',
    conversationId,
    '--markdown',
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'false',
  ] : [
    'chatgpt',
    'read',
    '--markdown',
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'false',
  ];
  const output = runOpenCli(readArgs, {
    profile: options.profile,
    timeoutMs: options.timeout * 1000,
  });
  const parsed = parseJsonFromOpenCli(output);
  return {
    parsed,
    output,
    conversationId,
    conversationUrl: conversationId ? `https://chatgpt.com/c/${conversationId}` : '',
  };
}

function askChatGpt(options) {
  const modelState = options.model
    ? parseJsonFromOpenCli(runOpenCli(
      ['chatgpt', 'model', options.model, '-f', 'json', '--site-session', options.siteSession],
      { profile: options.profile, timeoutMs: 120000 },
    ))
    : null;

  const makeAskArgs = (includeWebSearch) => {
    const askArgs = [
      'chatgpt',
      'ask',
      options.prompt,
      '--timeout',
      String(options.timeout),
      '-f',
      'json',
      '--site-session',
      options.siteSession,
      '--keep-tab',
      'false',
    ];
    if (options.conversation) askArgs.push('--conversation', options.conversation);
    else if (options.newConversation) askArgs.push('--new');
    if (includeWebSearch) askArgs.push('--web-search');
    if (options.deepResearch) askArgs.push('--deep-research');
    return askArgs;
  };

  const timeoutMs = (options.timeout + 45) * 1000;
  const wantsWebSearch = Boolean(options.search && !options.deepResearch);
  let output;
  let webSearchFallback = null;
  try {
    output = runOpenCli(makeAskArgs(wantsWebSearch), {
      profile: options.profile,
      timeoutMs,
    });
  } catch (error) {
    if (!wantsWebSearch || !shouldRetryWithoutExplicitWebSearch(error)) {
      throw error;
    }
    webSearchFallback = {
      requested: true,
      used: false,
      reason: 'OpenCLI explicit ChatGPT Web Search path failed; retried without explicit --web-search.',
      error: compactOutput(error.message || String(error), 1500),
    };
    output = runOpenCli(makeAskArgs(false), {
      profile: options.profile,
      timeoutMs,
    });
  }
  const parsed = parseJsonFromOpenCli(output);
  return { parsed, output, modelState, webSearchFallback };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }
  validateOptions(options);

  const startedAt = new Date().toISOString();
  const raw = options.captureCurrent ? captureCurrent(options) : askChatGpt(options);
  const answerText = extractAnswerText(raw.parsed);
  const questionText = options.prompt || extractUserMessage(raw.parsed);
  const conversation = extractConversation(raw.parsed);
  conversation.id = conversation.id || raw.conversationId || '';
  conversation.url = conversation.url || raw.conversationUrl || '';
  let status = null;
  if (!conversation.url) {
    try {
      status = getChatGptStatus(options);
      conversation.url = status.url || conversation.url;
      conversation.id = conversation.id || conversationIdFromUrl(status.url);
    } catch (error) {
      status = { error: error instanceof Error ? error.message : String(error) };
    }
  }

  const textReferences = collectReferencesFromText(answerText);
  let domReferences = null;
  let domReferenceError = '';
  try {
    domReferences = collectReferencesFromDom(options, conversation.url);
  } catch (error) {
    domReferenceError = error instanceof Error ? error.message : String(error);
    domReferences = {
      requested: true,
      count: 0,
      items: [],
      note: `DOM source extraction failed: ${compactOutput(domReferenceError, 1500)}`,
      raw: null,
    };
  }
  const references = mergeReferenceCollections([textReferences, domReferences], Boolean(options.search || options.deepResearch));
  if (!references.requested && references.count === 0) {
    references.note = 'Reference extraction was not requested because --no-search was used.';
  }
  if (raw.webSearchFallback?.reason) {
    references.note = [references.note, raw.webSearchFallback.reason].filter(Boolean).join(' ');
  }

  const record = {
    ok: Boolean(cleanText(answerText)),
    collected_at: new Date().toISOString(),
    engine: 'chatgpt',
    transport: 'opencli-chatgpt-adapter',
    question: questionText || '',
    options: {
      search: options.search,
      deep_research: options.deepResearch,
      model: options.model || null,
      profile: options.profile || null,
      site_session: options.siteSession,
      conversation: options.conversation || null,
      new_conversation: Boolean(options.newConversation && !options.conversation && !options.captureCurrent),
      capture_current: Boolean(options.captureCurrent),
      started_at: startedAt,
    },
    page: {
      url: conversation.url || null,
      title: 'ChatGPT',
      conversation_id: conversation.id || null,
    },
    answer: {
      text: answerText,
    },
    references,
    extraction: {
      char_count: answerText.length,
      line_count: answerText ? answerText.split(/\r?\n/).length : 0,
      headings: extractHeadings(answerText),
      reference_count: references.count,
      target: options.target ?? null,
      target_mention_count: countOccurrences(answerText, options.target),
    },
    raw: {
      opencli_result: raw.parsed,
      opencli_output_excerpt: compactOutput(raw.output),
      model_state: raw.modelState || null,
      tool: conversation.tool || null,
      status: status?.parsed || null,
      status_error: status?.error || null,
      web_search_fallback: raw.webSearchFallback || null,
      dom_references: domReferences?.raw || null,
      dom_reference_error: domReferenceError || null,
    },
  };

  if (options.out) {
    fs.mkdirSync(path.dirname(path.resolve(options.out)), { recursive: true });
    fs.writeFileSync(path.resolve(options.out), `${JSON.stringify(record, null, 2)}\n`);
  }
  console.log(JSON.stringify(record, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
