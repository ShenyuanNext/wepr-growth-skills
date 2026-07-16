---
name: xiaohongshu-title
description: Generate, diagnose, select, and rewrite Xiaohongshu post titles and cover lines for image-text posts, short videos, tutorials, comparisons, product content, service content, and search-oriented notes. Use when the user explicitly requests 小红书标题, 封面标题, 标题诊断, 标题优化, title directions, or multiple title candidates. Use plan-xiaohongshu-growth when the user also needs the full body, keywords, or a complete publishing-ready post.
---

# Create Xiaohongshu Titles

Create a truthful reason to open the post. Build titles from the user's actual scene, tension, decision, method, evidence, and search language—not from fabricated stories or formula stacking.

## Mode selection

- **Direct mode:** The user asks for a specific number of titles. Return that number and follow all length or tone constraints.
- **Exploration mode:** The user wants options or directions. Generate distinct strategic angles, then recommend one.
- **Diagnosis mode:** The user provides existing titles. Diagnose the precise weakness and rewrite it in the same direction and alternative directions.

Do not default to a large title dump when the user wants two or three usable options.

## Input extraction

Identify:

1. target reader and immediate situation;
2. content job: search answer, execution method, case, comparison, opinion, proof, or conversion;
3. primary keyword when search discovery matters;
4. strongest real detail: action, object, number, constraint, mistake, trade-off, or outcome;
5. body promise and evidence available;
6. tone, format, title-count, and length constraints.

Do not invent price, sales, followers, revenue, time, identity, experience, reviews, product results, platform policy, or third-party proof.

## Title angles

Use only angles supported by the content:

- audience + concrete problem;
- scene + unresolved tension;
- costly mistake + correction;
- counter-intuitive judgment + reason;
- number/checklist + execution object;
- comparison + decision rule;
- question phrased in the reader's language;
- experiment/case + method + boundary;
- short cover statement that creates recognition;
- search keyword + clear outcome or task.

Vary sentence structure. Do not generate synonyms of the same title.

## Quality rules

- Let the reader recognize the applicable situation quickly.
- Keep one promise per title.
- Preserve the primary keyword naturally when search matters; clarity is more important than stuffing.
- Leave enough unresolved value to justify opening, but do not use fake suspense.
- Make the title consistent with the cover and body.
- Keep titles within the user's specified limit. When the user requests a Xiaohongshu-native short-title constraint, count characters and prefer 6–18 Chinese characters; do not present this as an official platform rule.
- Use first person only when the source contains a real first-person experience and the requested account voice allows it.
- Avoid empty superlatives, guaranteed results, fake urgency, exaggerated scarcity, and sensitive-category promises.

## Style-risk filter

Rewrite titles that depend on formulaic filler such as “天花板、封神、闭眼入、被问爆、所有人都该、没人告诉你、建议收藏、狠狠拿捏” unless the user's verified voice and evidence clearly justify the wording. Treat this as an editorial filter, not a claim about platform policy.

Also reject repetitive contrast templates such as “不是 X 而是 Y” when the contrast adds no new information.

## Output

### Direct mode

Return the requested number of titles. When useful, group them by angle and mark the recommended title. Do not add an essay about the process.

### Exploration mode

Return:

1. three to five title directions and when each fits;
2. distinct candidates under each direction;
3. one recommended title;
4. one sentence explaining the choice;
5. the primary keyword and any promise-risk note.

### Diagnosis mode

Return:

1. the original title's specific problem;
2. three same-direction rewrites;
3. five alternative-direction rewrites;
4. one recommended title and reason;
5. any unsupported claim or body-delivery risk.

## Final check

Before returning, verify that every title comes from the supplied facts, differs materially from the others, has a clear subject, matches the desired reader, and can be fulfilled by the body.
