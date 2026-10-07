# ALL KONJAC website

Static international B2B website for https://allkonjac.com/. The deployed files are ordinary HTML, CSS, JavaScript and images. No server application or cloud build step is required.

## Public pages and languages

The English URLs remain unchanged:

- `/` — overview, buyer questions and contact details
- `/ingredients/` — konjac powder, refined powder and konjac gum
- `/equipment/` — food equipment and production-line engineering
- `/drying-lines/` — konjac dried-chip drying systems
- `/technology/` — hydrocolloid formulation and application development

The same five business pages exist under `/th/` for Thai and `/id/` for Indonesian, giving 15 business pages. Language links preserve the current business page. Internal navigation stays in the selected language. All shared assets use `/assets/` URLs, including local font files.

All 15 business pages use shared motion via `body.motion-enabled`. It provides a one-time gentle scroll reveal for titles and copy, staggered business cards, subtle card hover and clipped image zoom. English, Thai and Indonesian use identical behavior. Detail images retain their dimensions and margins; navigation, language controls and the trilingual 404 remain immediately readable. Without JavaScript, IntersectionObserver support, or with reduced motion enabled, content remains fully visible. Reduced motion changes, keyboard focus and printing also reveal pending content. No third-party animation dependency is required.

The single root `404.html` provides English, Thai and Indonesian explanations and return links. It carries `noindex,follow` and is not listed in the sitemap. The existing Wrangler `not_found_handling: "404-page"` configuration provides an actual 404 response for unknown paths rather than a 200 rewrite.

## Editing and generating

Python 3.9 or later is sufficient; only the standard library is used. From the repository root:

```text
python scripts/build.py --self-test
python scripts/build.py --check
python scripts/build.py
```

`--self-test` verifies all 15 template variants, URL and schema transformations, HTML/attribute/JSON escaping, strict missing-key rejection and sitemap count in memory. It can run while translations are being prepared and writes no placeholder translation pages. `--check` validates the complete three-language site in memory. The ordinary command writes the 15 HTML files, root trilingual 404, sitemap and llms.txt only after all inputs validate. It never publishes, installs packages, or contacts a translation service.

Generator inputs:

- `source/templates/*.html` — editable page templates copied from the approved English HTML; full paragraphs and questions remain intact
- `source/schema/*.json` — structured-data templates, using objects such as `{"$t": "stable_translation_id"}` for descriptive strings
- `content/en.json`, `content/th.json`, `content/id.json` — flat JSON objects with identical stable string IDs and non-empty string values
- `source/translation-context.json` — extraction locations for translators and reviewers
- `source/original/*.html` — the five original English pages retained as a reference
- `scripts/build.py` — deterministic static generator

The initial English catalog contains 233 unique strings. Descriptive metadata, alt/aria labels, structured-data descriptions, menu labels, hero overlay and 404 text are included. Duplicate English strings share one ID. Hash-shaped IDs are stable identifiers: keep them when editing an existing string, then update all three catalogs together. Add a new unique key for a new concept or sentence. Template tokens `{{t:ID}}` escape HTML text; `{{a:ID}}` escape HTML attributes. Translations are plain text and must not contain markup. Structured data is serialized with JSON escaping and script-termination protection.

Translations must preserve ALL KONJAC, WhatsApp, WeChat, contact details, URLs and numerical facts. The generator rejects incomplete catalogs, unexpected keys, empty values and changed protected contact/brand/numerical facts. It has no English fallback. Review Thai and Indonesian drafts from Google Translate against the original English and the technical glossary before generating pages; automatic drafts do not establish product specifications or business claims.

`scripts/extract_catalog.py` is the one-time bootstrap extractor. It refuses to replace an existing catalog. Do not rerun it over generated pages; future edits belong in the source templates, structured-data templates and catalogs. Direct edits to generated HTML will be replaced on the next generation. Shared presentation and progressive navigation enhancement remain in `assets/site.css` and `assets/site.js`.

## Discovery metadata

Every business page has its own translated title/description, canonical URL, HTML language and Open Graph locale. The language alternates are reciprocal `en`, `th`, `id` and `x-default`, with `x-default` pointing to the corresponding English business page. The sitemap lists all 15 URLs and the same alternates. There is no automatic IP or browser-language redirect.

Organization and WebSite IDs remain global. Organization contact facts stay unchanged. Page, service, item-list and breadcrumb identities and page links use the corresponding language URL. WebSite `inLanguage` declares all three languages. Descriptive structured-data strings are localized and must match visible business information. No unsupported certifications, capacity, customers, founding dates or performance guarantees may be added.

`llms.txt` is a factual index linking all 15 business pages. It is optional and does not guarantee search rankings or AI citations. `robots.txt` retains the existing crawling policy and points to the sitemap. Google Search Console work and indexing actions are paused for manual review; generation does not submit URLs or change Google settings.

## Hosting and review

The existing `wrangler.jsonc` still points at the root static files for the ALL KONJAC Worker. `.assetsignore` excludes catalogs, templates, scripts, audits, preparation material, dependencies and repository/deployment metadata from public assets. Keep those exclusions when changing the preparation workflow.

Before production publication, review the generated preview in all three languages and check desktop/mobile navigation, current-business-page language switching, long labels, typography, images and keyboard access. Confirm all 15 pages and assets return 200; unknown URLs must return 404. Production DNS, domain bindings and redirects remain separately managed in Cloudflare. This localization generator performs no preview or production deployment, commit, push or Google indexing action.

## Equipment image gallery (2026-10-07)

The three equipment pages share four AI-enhanced equipment images and translated captions/alt text. Original configuration, ratings and certifications are not inferred from generated pictures. The disclosure stays visible next to the gallery. Source and review records are in source/translations/equipment-gallery.json; new strings use the equipment.* namespace. The complete catalog now contains 253 strings per language.

The source template provides real full-size image links. A native dialog progressively enhances image viewing with Escape, focus restoration and backdrop dismissal. Without script or dialog support, links open the image normally. Cards share the existing one-time motion; the responsive grid uses two columns, one below 700px. Three WebP sizes (480/960/1448px) use srcset; PNG masters remain in the local project outputs and are not deployed. Images are encoded from the approved generated masters without further creative editing.
