# SEO Knowledge Freshness

SEO mixes durable web mechanisms with fast-changing product behavior. Treat them differently.

## Claim classes

| Class | Examples | Required handling |
|---|---|---|
| stable principle | HTTP behavior, crawl/render/index distinction, evidence semantics | cite when consequential; periodic review |
| current platform rule | supported rich result, crawler user agent, report/API behavior | official source, provider, reviewed date |
| observed market state | SERP layout, AI citation, competitor, ranking | market, device, login state, date, repeated sample when important |
| estimate | keyword volume, traffic, backlinks, difficulty | named provider/method/date; never present as ground truth |
| hypothesis | cause of traffic loss, expected change impact | test and alternatives; never report as observed fact |

## Source registry

`data/seo-source-registry.json` records official sources, topic, stability, review cadence, and known feature lifecycle notes. Run:

```bash
python3 scripts/validate_knowledge.py .
```

The validator checks structure, official-domain policy, duplicate sources, overdue reviews, and banned stale claims. It does not fetch the web or prove that the source still says the same thing.

When a relevant source is overdue or the task is time-sensitive:

1. open the official page
2. record the observation date and any documentation update date
3. compare related official pages for rollout or transition conflicts
4. update the registry/reference if the reusable rule changed
5. preserve the previous claim in the upgrade report only when useful for explaining the correction

## Conflict handling

When official documents disagree:

- prefer the newer, more specific product documentation for the named surface
- do not erase a broader older statement if both can be true
- state rollout, account availability, locale, or report-scope uncertainty
- avoid converting a product announcement into a universal implementation requirement

Example: a newer dedicated generative-AI performance report can coexist with generative-AI activity contributing to broader Web performance totals. Verify the current property rather than asserting only one view exists.

## Feature lifecycle labels

Use `experimental`, `limited`, `supported`, `deprecated`, or `removed`. A Schema.org type may remain valid after a search feature is deprecated; a Search Console dimension may remain during a transition. Name which layer changed.
