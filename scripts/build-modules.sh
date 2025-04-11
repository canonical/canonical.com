rm -rf static/js/dist
rm -rf static/js/modules

mkdir -p static/js/modules/cookie-policy
cp node_modules/@canonical/cookie-policy/build/js/cookie-policy.js static/js/modules/cookie-policy

mkdir -p static/js/modules/fuse
cp node_modules/fuse.js/dist/fuse.js static/js/modules/fuse

mkdir -p static/js/modules/latest-news
cp node_modules/@canonical/latest-news/dist/latest-news.js static/js/modules/latest-news

mkdir -p static/js/modules/global-nav
cp node_modules/@canonical/global-nav/dist/global-nav.js static/js/modules/global-nav

mkdir -p static/js/modules/intl-tel-input
cp node_modules/intl-tel-input/build/js/utils.js static/js/modules/intl-tel-input

mkdir -p static/js/modules/discourse-rad-parser
cp node_modules/@canonical/discourse-rad-parser/build/js/discourse-rad-parser.js static/js/modules/discourse-rad-parser

partytown copylib static/js/dist/~partytown