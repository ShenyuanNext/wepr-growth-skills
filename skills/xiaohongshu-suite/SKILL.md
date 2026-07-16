---
name: xiaohongshu-suite
description: Route and orchestrate Xiaohongshu account, profile, topic, title, comment, content, conversion, and review tasks. Use when the user wants an overall Xiaohongshu diagnosis or workflow but is unsure whether to start with positioning, profile, topic planning, titles, full-copy execution, comment operations, or conversion design. Route clear single-purpose requests to the matching xiaohongshu-* or plan-xiaohongshu-growth skill instead of duplicating their output.
---

# Xiaohongshu Workflow Router

Identify the blocked stage, select the shortest useful workflow, and pass forward the user's existing facts. Do not redo work that a specialist skill already owns.

## Route map

| User need | Primary skill |
| --- | --- |
| Overall account launch, repair, or operating system | `$launch-content-account` |
| Profile first impression, bio, identity, pinned posts | `$xiaohongshu-profile` |
| Topic pool, series, weekly or monthly calendar | `$xiaohongshu-topic-planner` |
| Titles, cover lines, title diagnosis | `$xiaohongshu-title` |
| Full post, keywords, rewrite, search-oriented content | `$plan-xiaohongshu-growth` |
| Comment replies, pinned comments, objections | `$xiaohongshu-comment-reply` |
| Content-to-profile-to-consultation path | `$xiaohongshu-conversion-path` |
| Public benchmark-account research | `$distill-creator-playbook` |
| Illustration plan for posts | `$plan-editorial-illustrations` |

## Diagnostic sequence

Check the earliest broken stage first:

1. **Audience and promise:** Is the account clear about who it helps and why it matters?
2. **Profile acceptance:** Can a visitor understand the role, proof, pinned content, and next step?
3. **Topic relevance:** Do topics match real questions, decisions, objections, and search language?
4. **Packaging:** Do title and cover create a relevant, truthful reason to open?
5. **Content delivery:** Does the body fulfill the promise with steps, evidence, boundaries, and takeaways?
6. **Conversation:** Do comment replies extend value and handle objections without scripted selling?
7. **Conversion:** Is the next step permitted, specific, low-friction, and appropriate to the offer?
8. **Review:** Are results diagnosed by stage instead of blamed on an unverified algorithm claim?

## Common workflows

- **New account:** `$launch-content-account` → `$xiaohongshu-profile` → `$xiaohongshu-topic-planner` → `$plan-xiaohongshu-growth` → `$xiaohongshu-comment-reply`.
- **Publish one post:** `$xiaohongshu-topic-planner` → `$xiaohongshu-title` → `$plan-xiaohongshu-growth` → `$xiaohongshu-comment-reply`.
- **Service or product acquisition:** `$xiaohongshu-profile` → `$xiaohongshu-conversion-path` → `$xiaohongshu-topic-planner` → `$plan-xiaohongshu-growth`.
- **Low activity or weak inquiries:** `$plan-xiaohongshu-growth` diagnosis → repair the earliest failed stage → run a comparable content sample.

## Output

When the request is ambiguous, return:

1. the blocked stage and supporting evidence;
2. the first skill to use and why;
3. the processing order;
4. the known inputs carried forward;
5. only the missing inputs that materially change the result.

When the request is clear, use the matching specialist skill directly.

## Guardrails

Do not promise views, ranking, follower growth, inquiries, sales, or permanent search placement. Do not recommend fabricated identity, copied posts, hidden advertising, coordinated engagement, ban evasion, or coded off-platform diversion. Verify current official rules before advising on advertising, commerce, external links, private messages, AI labels, or sensitive categories.
