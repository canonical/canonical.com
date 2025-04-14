// const { purgeCSSPlugin } = require("@fullhuman/postcss-purgecss");
const purgeCSSPlugin = require("@fullhuman/postcss-purgecss");

const isDev = process && process.env && process.env.NODE_ENV === "development";
console.log("🚀 ~ isDev:", isDev);

/** @type {import('postcss-load-config').Config} */
let config = {
  plugins: [require("autoprefixer")],
};

// Only purge in production
if (!isDev) {
  config.plugins.push(
    purgeCSSPlugin({
      content: [
        "templates/**/*.html",
        "static/js/**/*.js",
        "webapp/js/**/*.py",
      ],
      defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
    })
  );
}
// let purgeConfig = {};
// // Only purge in production
// if (!isDev) {
//   purgeConfig = {
//     content: ["templates/**/*.html", "static/js/**/*.js", "webapp/js/**/*.py"],
//     defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
//   };
// }

module.exports = config;
