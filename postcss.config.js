const { purgeCSSPlugin } = require("@fullhuman/postcss-purgecss");

const isDev = process && process.env && process.env.NODE_ENV === "development";

let purgeConfig = {};
// Only purge in production
if (!isDev) {
  purgeConfig = {
    content: ["templates/**/*.html", "static/js/**/*.js", "webapp/js/**/*.py"],
    defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
  };
}

/** @type {import('postcss-load-config').Config} */
module.exports = {
    plugins: [require("autoprefixer"),
        purgeCSSPlugin(purgeConfig)
    ],
};
