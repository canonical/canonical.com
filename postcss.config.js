const purgeCSSPlugin = require("@fullhuman/postcss-purgecss");

/** @type {import('postcss-load-config').Config} */
let config = {
  plugins: [
    require("autoprefixer"),
    purgeCSSPlugin({
      content: [
        "templates/**/*.html",
        "templates/**/*.jinja",
        "static/js/**/*.js",
        "webapp/js/**/*.py",
      ],
      defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
    }),
  ],
};

module.exports = config;
