const purgeCSSPlugin = require("@fullhuman/postcss-purgecss");

/** @type {import('postcss-load-config').Config} */
let config = {
  plugins: [
    require("autoprefixer"),
    purgeCSSPlugin({
      content: [
        "templates/**/*.html",
        "templates/**/*.jinja",
        "static/**/*.js",
        "static/**/*.tsx",
        "webapp/**/*.py",
        "templates/**/*.md",
        "templates/**/*.py",
        "templates/**/*.xml",
        "static/*.js",
        "static/*.jsx",
        "static/*.md",
        "static/*.tsx",
        "static/*.xml",
        "node_modules/flickity/dist/flickity.pkgd.min.js",
        "node_modules/leaflet/dist/leaflet.js",
        "node_modules/venobox/dist/venobox.min.js",
        "node_modules/vanilla-framework/templates/_macros/*.jinja"
      ],
      defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
      safelist: {
        standard: [
          /^cookie-policy/,
          /^form/,
          /^p-/, // Preserve form related classes
          /^u-/, // Utility classes
          /^js-/, // JavaScript-related classes
          /^leaflet-/, // Leaflet classes for map
          /^vbox-/, // VenoBox classes
          /^venobox/, // VenoBox classes
        ],
        greedy: [
          /^iti/,
          /^mktoForm/, // Marketo forms
          /^cc-/, // Cookie consent related
          /^optanon/, // Cookie consent related
          /^has-/, // State-related classes
        ],
        deep: [/form-.+/],
        keyframes: true,
        variables: true,
      },
    }),
  ],
};

module.exports = config;
