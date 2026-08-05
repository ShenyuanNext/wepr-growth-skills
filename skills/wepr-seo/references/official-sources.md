# Official SEO Sources

Last reviewed: 2026-08-03.

The machine-readable source of truth is `data/seo-source-registry.json`. It contains review cadence, topic, provider, lifecycle notes, and current stale-claim guards. Validate it with:

```bash
python3 scripts/validate_knowledge.py .
```

Use current official documentation for mutable policies and implementation behavior. Re-open the relevant page instead of relying only on this human index.

- Google Search Essentials: https://developers.google.com/search/docs/essentials
- SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Generative AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Debugging Search traffic drops: https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops
- Crawling and indexing overview: https://developers.google.com/search/docs/crawling-indexing
- JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Fix Search-related JavaScript problems: https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript
- Robots.txt introduction: https://developers.google.com/search/docs/crawling-indexing/robots/intro
- Robots meta and X-Robots-Tag: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- Title links: https://developers.google.com/search/docs/appearance/title-link
- Snippets: https://developers.google.com/search/docs/appearance/snippet
- Structured data introduction: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Structured data general guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Core Web Vitals: https://web.dev/articles/vitals
- Bing Webmaster Guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- Bing sitemap guidance: https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search
- IndexNow protocol: https://www.indexnow.org/documentation
- Schema.org Markup Validator: https://schema.org/docs/validator.html
- OpenAI crawlers: https://developers.openai.com/api/docs/bots
- OpenAI publisher FAQ: https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
- Perplexity crawlers: https://docs.perplexity.ai/docs/resources/perplexity-crawlers

When Google and another search engine differ, describe the engine-specific behavior instead of presenting one rule as universal.
