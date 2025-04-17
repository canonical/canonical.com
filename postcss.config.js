const purgeCSSPlugin = require("@fullhuman/postcss-purgecss");

/** @type {import('postcss-load-config').Config} */
let config = {
  plugins: [
    require("autoprefixer"),
    // purgeCSSPlugin({
    //   content: [
    //     "templates/**/*.html",
    //     "templates/**/*.jinja",
    //     "static/**/*.js",
    //     "static/**/*.tsx",
    //     "webapp/**/*.py",
    //     "templates/**/*.md",
    //     "templates/**/*.py",
    //     "templates/**/*.xml",
    //     "static/*.js",
    //     "static/*.jsx",
    //     "static/*.md",
    //     "static/*.tsx",
    //     "static/*.xml",
    //   ],
    //   defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
    //   safelist: {
    //     standard: [
    //       /^cookie-policy/,
    //       /^form/,
    //       /^p-/,  // Preserve form related classes
    //       /^u-/,  // Utility classes
    //       /^js-/  // JavaScript-related classes
    //     ],
    //     greedy: [
    //       /^iti/,
    //       /^mktoForm/,  // Marketo forms
    //       /^cc-/,      // Cookie consent related
    //       /^optanon/,  // Cookie consent related
    //       /^has-/      // State-related classes
    //     ],
    //     deep: [/form-.+/], // Classes that start with form- and have more segments
    //     keyframes: true,    // Preserve all keyframe animations
    //     variables: true     // Preserve CSS variables
    //   }
    // }),
  ],
};

module.exports = config;
