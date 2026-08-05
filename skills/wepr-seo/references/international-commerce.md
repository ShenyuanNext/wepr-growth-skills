# International And Commerce SEO

## International sites

- Prefer stable, crawlable URLs for each language/region version rather than cookie- or browser-only switching.
- Determine page language from useful visible content; do not rely on `lang` or `hreflang` as a substitute for localization.
- Use valid language and optional region codes. A country code alone is not a language target.
- Every alternate set should include self-reference and reciprocal relationships; add `x-default` only when a genuine fallback/selector exists.
- Keep hreflang, canonicals, redirects, indexability, and sitemaps aligned. A localized page normally canonicalizes to itself, not mechanically to a different-language original.
- Avoid forced IP/language redirects that hide alternatives from users or crawlers. Provide accessible switching.
- Research intent, terminology, regulation, price, units, cultural expectations, and SERPs per market; translation alone is not keyword research.

## Ecommerce architecture

Make products reachable through crawlable category/subcategory/product links. Sitemaps and merchant feeds supplement navigation; they do not replace it.

For pagination, load-more, and infinite scroll:

- give each crawlable page a stable URL when content spans multiple result sets
- expose sequential `<a href>` links because crawlers generally do not click interaction controls
- avoid canonicalizing every paginated page to page one when the pages contain distinct products
- manage filter and sort combinations intentionally; prevent unbounded URL generation

## Products and variants

- Decide whether each variant deserves a separate URL from user intent, availability, content, links, and operational needs.
- Keep selected variant, URL, canonical, price, availability, images, and structured data consistent.
- Use current Google Product/ProductGroup documentation when implementing variant markup; supported properties and merchant requirements change.
- Mark up only visible, truthful offers, reviews, ratings, shipping, returns, identifiers, and availability.
- Validate Schema.org syntax and Google feature eligibility separately.

## Feeds, organic results, and shopping

Keep these evidence systems distinct:

- website HTML/rendered product content
- Product structured data
- Google Merchant Center or other merchant feeds
- organic web/search performance
- free listings or shopping surfaces
- paid Shopping campaigns

Price, availability, identifiers, URLs, and policy data should agree across applicable systems. A feed approval does not prove organic indexing; Product markup does not guarantee merchant or rich-result appearance; paid visibility is outside this skill unless the user explicitly asks only for an interface dependency.

## Inventory states

For out-of-stock, discontinued, replaced, seasonal, and temporarily unavailable products, decide from user value and likely return:

- keep live with accurate availability and alternatives
- redirect only to a genuinely equivalent replacement
- retain an informative archived page when it has durable value
- return `404` or `410` when removed without replacement

Avoid redirecting every discontinued product to a category or homepage.

Source anchors: Google international, ecommerce navigation, pagination, product variants, structured-data, Merchant Center, and spam-policy documentation in `data/seo-source-registry.json`.
