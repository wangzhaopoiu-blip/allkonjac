# ALL KONJAC website

## Approved image watermark (2026-10-12)

Every public business image embeds the approved Tian Ran Xing logo, rotated -30 degrees, at 20% opacity and 25% of the image's short edge, in a staggered repeating pattern. All responsive WebP sizes, full-size gallery images, background images and social-preview pictures are covered. Image URLs, dimensions and formats stay unchanged. The company logo, WeChat QR and language flags are exempt.

`source/image-watermark.json` records approved original/output hashes and the complete image inventory. `scripts/build.py` checks these hashes before rendering; new or changed images must be classified and watermarked before a build succeeds. Run `python scripts/check_watermarks.py` for a standalone check.

Regenerate with `node scripts/watermark-assets.cjs <private-original-assets-directory> <browser-executable>` using Node.js, Playwright and a Chromium-based browser. If needed, `ALL_KONJAC_NODE_MODULES` points at an existing dependency directory. The private input directory has the same relative image paths as `assets/`. The script always uses retained originals, verifies existing outputs and does not stack watermarks. Keep private originals and backups outside this repository and public deployment directory. Regeneration requires deliberate review of any changed originals or image inventory. Previously saved unwatermarked pictures cannot be recalled.

## Interactive equipment exterior view (2026-10-12)

The English, Thai and Indonesian equipment pages share an exterior 3D reference visualization. The viewer loads automatically and gently rotates while in view. Leaving the section or switching browser tabs pauses drawing and rotation; returning resumes the visitor's selected rotation state. Reduced-motion preferences start still. Dragging, view presets and zoom allow closer inspection, with accessible pause/reset controls and keyboard rotation. Unsupported WebGL falls back to the equipment image.

This model is an exterior visualization with relative proportions. It does not define the dimensions, rating, exact configuration or internal operation of any listed product. Existing reference specifications, contacts and the other business pages are maintained independently. Original videos, workshop reference photos and local source notes are excluded from public assets.

Editable UI, geometry and viewer code are in `source/data/equipment-3d-*.json` and `source/equipment3d/`. Shared section styles and initialization are in `assets/equipment-3d.css` and `assets/equipment-3d.js`. Three.js 0.180.0 and esbuild 0.25.10 are pinned for the viewer build. Supply an installed runtime containing those packages with `node scripts/build_equipment_3d.mjs --runtime <runtime-root>`, then run the normal site generator. The generated viewer assets stay committed, so production hosting still needs only the existing static asset deployment.

The loading/fallback poster follows the current approved image-watermark rules. Retain its unwatermarked original outside the repository and run `node scripts/watermark-equipment3d-poster.cjs <private-original-poster>` after regeneration; this updates only the new poster and its inventory entry. For a reviewed model revision, retain the previous original and use `--replace-reviewed-poster` to replace the inventory entry. PNG and WebP originals are supported; the public output stays WebP. `EQUIPMENT_PLAYWRIGHT_MODULE` can select an existing local Playwright installation. The live 3D rendering remains an exterior visualization and does not assign a manufacturer or reference specification.

The v003 static blade slopes downward from its outer support into the hopper. The user confirmed the direction and requested retaining the provisional 12-degree angle; it has not been measured. Blade guides, supports and a narrow wall passage follow that geometry. No cutting stroke is simulated. Whole-machine exterior acceptance remains pending. Browser verification can use `EQUIPMENT_WEBGL_BACKEND=d3d11` when the installed browser cannot initialize its SwiftShader backend.

`scripts/verify_equipment_3d.cjs --out <QA-directory>` checks automatic loading, rotation, views, input, visibility, mobile simulation and fallback behavior against a local HTTP preview. Pass `--url` or `--playwright-module` for another local runtime. Offline review exports are separate copies with `noindex,nofollow`; they are not production assets.

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

## English equipment reference configurations (2026-10-08)

The card layout was first published on the English equipment page and accepted by the user. The Thai and Indonesian equipment pages now use the same nine four-field cards and balanced overview images. Maintain records in source/data/equipment-reference-en.json, equipment-reference-th.json and equipment-reference-id.json; labels, captions and alt text are in source/translations/equipment-reference.json. scripts/equipment_reference.py validates matching counts, numeric facts and technical tokens, escapes text and keeps enquiry links in the current language. Run scripts/build.py after edits. Shared fragment slots in source/templates/equipment.html and assets/equipment-reference.css apply to the three equipment pages. Locale-specific typography preserves the accepted English layout.

Dimensions keep the supplied order; power is listed per reference configuration, not inferred as per-machine or whole-line power. Only supported material details appear in remarks; no steel grades are assumed. Incomplete units, tray thickness conflicts and uncertain equipment attribution remain excluded. Contract identities, contacts, quantities, prices, commercial terms and the source DOCX must never be committed or deployed. Existing public website contacts are maintained separately. Gallery images illustrate equipment categories, not an exact model or specification. The overview uses an aligned 4:3 image pair and stacks below 900px.

The new reference translations were reviewed against the accepted English page. Google Translate browser access timed out twice, so no Google-generated draft is claimed for these new strings. Method and terminology notes are in source/translations/equipment-reference-provenance.json. The earlier site's Google draft records describe their own historical translation phase. Unconfirmed technical details stay excluded in every language. Manual Google Search Console indexing remains paused.
