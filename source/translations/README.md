# Translation provenance and review

The English baseline is `content/en.json` (233 unique full strings, including metadata, structured-data descriptions, accessibility labels and 404 text). Context locations are recorded in `source/translation-context.json`.

`google-th.json` and `google-id.json` record actual results read from the official Google Translate text webpage, with English selected as the source and Thai or Indonesian selected as the target. Each accepted input batch contained 3,936, 3,861, 3,927, 3,745 or 3,374 characters, including numeric alignment markers. There were five accepted batches per language. A browser input that accidentally appended to the preceding batch was discarded and resubmitted after clearing the source field; it is not part of the draft catalog.

Numeric alignment markers were removed when assembling the catalogs; layout-only whitespace was normalized. Every source key has a Google draft and a reviewed result. The reviewed website catalogs are `content/th.json` and `content/id.json`; initial machine mistakes remain visible in the comparison record.

The assistant checked all strings against the English source for terminology, meaning, business conditions, omissions and protected brand/contact/numeric facts. This is an assistant-reviewed translation, not a claimed native-speaker or certified translation. No new species, certifications, purity values, capacity claims or guaranteed results were added. Konjac is not automatically renamed porang. Refined powder denotes processing, not a claim of 100% purity; gum denotes the food hydrocolloid, not chewing gum. Installation and engineering commissioning are distinct services whose scope remains subject to the quotation.

The local preview has not been accepted for publication. Production deployment and Google Search Console indexing work remain paused. Browser layout and keyboard checks are pending because a saved browser permission blocks local preview access; Cloudflare's local workerd also failed to start on this Windows host.
