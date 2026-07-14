---
name: plan-editorial-illustrations
description: Turn Chinese or English articles into coherent editorial illustration systems, shot lists, prompts, and visual QA plans. Use for 文章配图, 小红书配图, 公众号插画, editorial illustration, illustration prompts, visual storytelling, recurring character systems, or checking composition, text accuracy, hierarchy, and style consistency.
---

# Plan Editorial Illustrations

Translate ideas into visual actions. Do not decorate every paragraph.

## Workflow

1. Read the complete source and identify the audience, publication surface, aspect ratio, illustration count, brand constraints, and required recurring character or style.
2. Extract the article's central thesis, key turns, abstract mechanisms, and moments that benefit from visual explanation.
3. Select only illustration-worthy moments. Prefer scenes that clarify tension, sequence, comparison, system, or consequence.
4. Create a shot list before generation: purpose, scene, subject action, composition, labels, color accents, and placement.
5. Assign one dominant visual structure per image: single action, before/after, path, balance, funnel, loop, ladder, or contrast.
6. Keep a consistent visual grammar across the set while varying composition and action.
7. Write generation prompts that specify canvas, hierarchy, character action, environment, text limits, palette, line quality, whitespace, and exclusions.
8. Generate immediately when the user explicitly requests images and an image tool is available; otherwise return prompts and a shot list.
9. Inspect every result for text errors, hierarchy, cropping, duplicated limbs, inconsistent character identity, crowded labels, and accidental commercial-slide styling.
10. Revise failed images individually rather than regenerating the whole set without diagnosis.

## Default visual direction

When the user requests a restrained hand-drawn editorial style but gives no brand guide, use a clean light background, black imperfect linework, large whitespace, one clear action, and sparse accent colors. Do not copy a living artist's or third party's signature style or protected character.

## Route by need

- Read [references/shot-list.md](references/shot-list.md) to select scenes and structure a set.
- Read [references/prompt-and-qa.md](references/prompt-and-qa.md) to write prompts and review outputs.

## Output standard

Return the relevant subset of: visual concept, illustration count, placement map, shot list, production prompts, negative constraints, alt text, and QA findings. Keep in-image text short and reproduce names, numbers, and quotations exactly from verified source material.
