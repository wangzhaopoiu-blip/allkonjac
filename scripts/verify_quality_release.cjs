// The former English-only release check is superseded by the trilingual check.
if (process.argv[2]) process.env.ALL_KONJAC_PREVIEW_URL = process.argv[2];
require('./verify_unified_release.cjs');
