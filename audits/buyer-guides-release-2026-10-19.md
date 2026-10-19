# ALL KONJAC buyer guides: release record

Date: 2026-10-19 (Asia/Shanghai). Cloudflare Worker `allkonjac` version `5c01df4f-8c1f-412f-8df2-4f1e7d030f7a` deployed from this checkout with Wrangler 4.147.0. The three buyer-guide drafts were merged into the already published KGM journal instead of replacing it. Their `datePublished` and `dateModified` reflect this publication date.

Published guide URLs:

- https://allkonjac.com/blog/choose-konjac-powder-gum/
- https://allkonjac.com/blog/konjac-equipment-project-brief/
- https://allkonjac.com/blog/plan-konjac-dried-chip-drying-line/

The Blog index links the two original research articles and all three buyer guides. The relevant English ingredients, equipment and drying-line pages link directly to their guide. Thai and Indonesian business pages retain their existing navigation; no untranslated Blog alternates were declared. The sitemap has 21 canonical URLs, and `llms.txt` indexes all six Blog URLs.

Evidence scope: `source/blog/evidence.json` maps buyer-guide business statements to first-party ALL KONJAC pages. These pages document the site's stated consultation scope, not independently verified product performance. No new image was published with these guides. Unverified certification, capacity, legal-entity relationship, client or energy claims were not added.

Verification: `python scripts/build.py --self-test`, `--check`, and the normal build passed. A local HTTP preview returned 200 for all six Blog pages, with one H1, expected canonical, internal links and visible/schema publication dates. A 603-pixel browser preview showed the index and an article without horizontal overflow. After deployment, all 15 business pages and six Blog pages returned 200 on `allkonjac.com`; the three guides had `BlogPosting` dates matching the visible date; sitemap, internal links and `llms.txt` were checked; an unknown Blog path returned 404. This establishes publication and technical availability, not search indexing or AI citation performance. No Search Console indexing request or external backlink placement was made.
