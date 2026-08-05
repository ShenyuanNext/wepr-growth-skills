# Image And Video Search

Load this module only when images or videos are material acquisition surfaces.

## Images

- Use standard HTML image elements with a crawlable `src`; CSS background images are not an equivalent discovery path for Google Images.
- Provide responsive `srcset`/`picture` where useful, with an `img src` fallback.
- Write alt text for the image's user purpose and context, not as a keyword container. Decorative images may need empty alt text.
- Keep important image URLs stable and accessible; verify CDN host ownership/access when diagnostics matter.
- Balance quality, dimensions, and compression; inspect the actual LCP image when performance is affected.
- Use image sitemaps or structured metadata only when they solve a discovery or rights/context need.
- Treat filenames and formats as implementation details, not ranking scores.

## Video

- Use a dedicated watch page when video is the page's primary purpose and the business wants video search features.
- Make the watch page, embed, thumbnail, and—where required—the video bytes accessible and stable.
- Keep VideoObject, video sitemap, Open Graph, title, description, duration, thumbnail, live state, and visible page content consistent.
- Provide a high-quality crawlable thumbnail and a meaningful text context/transcript where it serves users.
- Validate that JavaScript players expose discoverable metadata and do not require unsupported interaction before the video is identifiable.
- Separate video indexing from ordinary web-page indexing; monitor the relevant Search Console reports/search types.

## Vertical evidence rule

Search appearance is surface-specific. A page can be indexed as a web result but ineligible for an image, video, news, shopping, local, or other feature. Name the surface, eligibility evidence, observed appearance, market/device/date, and measurement source.

Source anchors: Google Image SEO, Video SEO, structured-data guidelines, sitemaps, and Search Console documentation in `data/seo-source-registry.json`.
