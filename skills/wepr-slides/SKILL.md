---
name: wepr-slides
description: 创建和编辑单文件 .bento.html 演示文档，文档内容以 JSON 形式保存在“#bento-doc”脚本块中。适用于从零制作演示文稿、根据现有资料生成方案，或优化已有 .bento.html 文件；可用于客户方案、报价展示、策略汇报和复盘材料。
---

# WEPR 单文件交互式演示

Use `$wepr-presentation-workbench` first when the user has not chosen between editable PPTX and single-file HTML, or when the task needs narrative planning, template selection, presenter notes, client-deck structure, and cross-format delivery QA. This skill owns only the Bento HTML route.

For WEPR proposals, strategy decks, quotation presentations, quarterly reviews,
and client reports, first read `references/wepr-delivery.md`. Keep claims,
figures, pricing, platform scope, and source dates consistent with the approved
source document or spreadsheet.

A Bento deck is one self-contained `.bento.html` file. The document is plain
JSON in a single block:

```html
<script type="application/bento+json" id="bento-doc"> { "format":"bento/slides", ... } </script>
```

You edit **that block only**, in place. Escape every `<` in the JSON as
`\u003c` so it can never contain a literal `</script>`. Leave the rest of the
file (the compressed runtime) untouched. In a chat context instead, the user
copies the JSON out (*Save ▾ → Copy document JSON*) and pastes your
replacement back (*Save ▾ → Replace from JSON…*); `window.bento.loadDoc(json)`
does it from the console.

## Starting from nothing

Fresh `.bento.html` authoring requires a compatible shell supplied by the user
or already available in the workspace. Verify that it contains `id="bento-doc"`,
then write the document into that block. Never download an external project or
runtime without the user's explicit request. If no compatible shell exists,
route the task to `$wepr-presentation-workbench` and create a self-contained
HTML or editable PPTX deliverable instead.

Current shells may contain an empty block; a showcase visible on first browser
open can be generated at runtime and is not proof that the on-disk file already
contains document JSON. Never discard existing JSON without parsing and
preserving it first.
Use `python3 scripts/wepr_deck.py inject <deck.bento.html> <document.json>`
for deterministic replacement and `python3 scripts/wepr_deck.py validate
<deck.bento.html>` before delivery. Current shells may contain an empty
`#bento-doc` block; that is valid and ready for injection.
Rules for a fresh document:

- Start from the compatible shell's existing document contract. `size` and `theme` (including
  `theme.fontFamily`) are **required** — the app will not boot without them.
- **Fully specify element fields** as the skeleton shows (shapes need
  `stroke`/`strokeWidth`; text needs `fontFamily`/`align`/`valign`) — missing
  fields render wrong or not at all.
- **Omit `docId` and `collab` entirely**: the app mints a fresh identity and
  dormant collaboration credentials on first open.

## Current format capabilities

The `bento/slides` v1 document format is additive. Inspect the supplied shell
and preserve unknown keys rather than deleting them. Current compatible shells
may support:

- `code` elements with syntax highlighting and line-aware morphing;
- deck-level `present.morphSeconds` between `0.1` and `6` seconds;
- reusable deck brand colours and `theme.chartPalette`;
- `morphId` when the semantic match should differ from the element `id`;
- linked table-to-chart data, state slides, hidden slides, media, comments,
  collaboration, validation, and text measurement.

Use a feature only when the target shell accepts it. Unknown fields may be
ignored silently, so runtime validation and visual review remain mandatory.

When done, offer to open it (`open` / `xdg-open` / `start`) — the file boots
straight into the editor with the finished deck. Aim for one pass from
request to opened deck.

## Workflow

1. **Find the document.** Locate the `#bento-doc` block; parse its JSON. Note
   `doc.size` (canonical 1280×720), `doc.theme`, existing element `id`s, and
   whether `doc.template`/`doc.readonly` are set.
   Check `doc.collab` before sharing, copying, or returning JSON. If it contains
   owner, writer, or invitation secrets, warn the user that anyone receiving
   the file or JSON may be able to modify the live session. Offer a read-only
   duplicate or key rotation; do not imply that deleting keys from the current
   copy revokes access already shared elsewhere.
2. **Read the source material the user gave you** and classify each piece —
   is it a stat? a table? a process? a definition to expand? a photo?
3. **Map material → feature (do NOT default to bullet text).** This is the
   step that makes it a Bento deck rather than a slideshow of paragraphs:
   - numbers to compare visually (trend, magnitude, share) → a **chart** element
   - a comparison / spec / pricing / feature grid → a **table** element
     (`columns` weights + `rows` of `cells` + a `style` object)
   - consecutive slides about the **same thing changing** → **morph**: give
     shared elements the same `id` on both slides + `transition:"morph"` on
     the later one (Bento's signature move — reach for it liberally)
   - a point to **drill into** → a **state slide** (`stateOf` + element `link`)
   - a **hero / full-slide image** → full-bleed image + scrim rect + text,
     with **ken-burns** drift
   - a **sequence / flow / timeline** → a line/`path` with a `dash-march`
     loop, or morph a highlight through the steps
   - a **headline number** → big text + `fx:{countUp:true}`
   - **every cover / divider** → at least one ambient motion
   - **repeated chrome / logo** → keep its `id` stable across slides so it
     morphs in place
   - a **demo clip / recording / soundbite** → a **media** element
     (`kind: video|audio`); embed short clips as a data URI, link big ones by
     URL to keep the file small
4. **Author** using the schema already present in the compatible shell or the
   user's supplied format documentation. Respect one
   accent colour, ≤2 typefaces, 96px side margins (right-most x ≤ 1184),
   and write **speaker notes** on each slide.
5. **Self-audit before finishing:**
   - [ ] any numbers rendered as text that should be a **chart**?
   - [ ] do consecutive slides on one subject share **ids + `transition:"morph"`**?
   - [ ] at least one **motion moment** (ken-burns / loop / count-up), esp. the cover?
   - [ ] a drill-down that would work better as a **state slide**?
   - [ ] one accent colour, ≤2 typefaces, 96px margins?
   - [ ] speaker notes on every slide?
6. **Write back** the edited `#bento-doc` block (escaping `<`), or return the
   replacement JSON. Never regenerate the whole HTML file.
7. **Validate** with `scripts/wepr_deck.py validate`, then open the file in a
   browser and review every slide, interaction, chart, note, and margin.
   Confirm the saved filename and location so a returning user does not mistake
   a new browser starter for the previously saved deck.

When the open shell exposes `window.bento.validate()`, run it and inspect every
non-information finding. When it exposes `window.bento.measure()`, use the real
renderer to size long text before placement instead of estimating box height.

## Critical gotchas

- **Charts:** bar/line series `data` must be **plain numbers** (`{value,…}`
  item objects coerce to 0 — only pie takes `{name,value}`); colour by
  series, not per bar; `option` is pure JSON, template formatters only
  (`{b}`/`{c}`/`{d}`), never functions.
- **Morph needs deterministic, stable ids** shared across the slides that
  should animate together. Different ids = no morph (elements just cut).
- **Images/fonts must be embedded** as data URIs in `doc.assets` and
  referenced by `"asset:<key>"` — the file stays self-contained.
- **Media:** a `media` element (`kind: video|audio`) embeds short clips as a
  data URI in `src` (self-contained) or references a URL for big files (keeps
  the deck small). `autoplay` runs only in present mode and needs `muted:true`
  for video. Don't embed large videos — they bloat the file.
- **Never regenerate `docId`** when editing an existing deck; it is the
  document's identity. (Fresh decks omit it — the app mints one.)
- `template:true` → every open mints a fresh deck; `readonly:true` → the
  file boots straight into the show with no editor.
- Pair foreground colors with the actual surface/theme tokens they sit on.
  Inspect light and dark modes when theme switching is available.
- Surface parsing, export, save, rendering, and media failures. An empty result
  or swallowed exception must not be reported as a completed deck.

Use only templates already supplied by the user or included in the authorized
workspace; do not add external project links or copied runtime packages.
