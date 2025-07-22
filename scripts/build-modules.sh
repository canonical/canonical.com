rm -rf static/js/dist
rm -rf static/js/modules

mkdir -p static/js/modules/cookie-policy
cp node_modules/@canonical/cookie-policy/build/js/cookie-policy.js static/js/modules/cookie-policy/cookie-loader.js

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

mkdir -p static/js/modules/flickity
cp node_modules/flickity/dist/flickity.pkgd.min.js static/js/modules/flickity

mkdir -p static/js/modules/leaflet
cp node_modules/leaflet/dist/leaflet.js static/js/modules/leaflet

mkdir -p static/js/modules/venobox
cp node_modules/venobox/dist/venobox.min.js static/js/modules/venobox/venobox.min.js

mkdir -p static/js/modules/vanilla-framework
cp -r node_modules/vanilla-framework/templates/_macros/ static/js/modules/vanilla-framework
