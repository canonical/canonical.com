module.exports = {
  entry: {
    main: [
      './static/js/dynamic-image-load.js',
      './static/js/find-a-partner.js',
      './static/js/highlight-nav-on-scroll.js',
      './static/js/modal.js',
      './static/js/navigation.js'
    ],
    careers: [
      './static/js/apply-for-jobs.js',
      './static/js/careers-filter-and-sort.js',
      './static/js/careers-game.js',
      './static/js/file-validation.js',
      './static/js/tabs.js',
    ]
  },
  output: {
    filename: '[name].min.js',
    path: __dirname + '/static/js/build'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env']
        }
      }
    ]
  }
 };