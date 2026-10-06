# ALL KONJAC website

Static international B2B website for https://allkonjac.com/.

## Public pages

- / — overview, buyer questions and contact details
- /ingredients/ — konjac powder, refined powder and konjac gum
- /equipment/ — konjac food equipment and production-line engineering
- /drying-lines/ — konjac dried-chip drying systems
- /technology/ — hydrocolloid formulation and application development

No build step is required. Shared styles and navigation are in assets/site.css and assets/site.js. Keep the existing Cloudflare deployment pointed at the repository's static files.

## Search and AI discovery

Each page has its own title, description, canonical URL and share metadata. Visible content is delivered as HTML, with Organization, WebSite, WebPage, Service, ItemList and BreadcrumbList JSON-LD where relevant. robots.txt allows crawling under the existing policy; sitemap.xml lists the five canonical pages. llms.txt is an optional factual index for tools that support it and is not a ranking mechanism.

Before publishing new content, verify specifications and business claims. Do not add certifications, capacity, customers, founding dates or performance guarantees without confirmation. Structured data must match the visible content.

## Deployment checks

Confirm all five pages and their assets return 200. Unknown URLs must return 404. Check redirects from HTTP and HTTPS www.allkonjac.com to https://allkonjac.com, including paths and query strings. DNS and Redirect Rules are managed in Cloudflare and are not created by these HTML files.

Verify the domain in Google Search Console, submit https://allkonjac.com/sitemap.xml, and inspect the five URLs. Check Cloudflare crawler policies and challenges separately: robots.txt cannot override a CDN block.

Multi-language pages are deferred. No hreflang is declared for unpublished translations.
