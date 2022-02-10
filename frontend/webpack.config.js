const path = require('path')
const webpack = require('webpack')
module.exports = {
  // Where Webpack looks to load your JavaScript
  entry: {
    index: path.resolve(__dirname, 'src/index.js'),
    search: path.resolve(__dirname, "src/search.js"),
    titles: path.resolve(__dirname, 'src/titles.js'),
  },
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
      },
    ]
  },
  // Where Webpack spits out the results (the myapp static folder)
  output: {
    path: path.resolve(__dirname, '../backend/backend/myapp/static/myapp/'),
    filename: '[name].js',
  },
  plugins: [
    // Don't output new files if there is an error
    new webpack.NoEmitOnErrorsPlugin(),
  ],
  // Where find modules that can be imported (eg. React) 
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: [
        path.resolve(__dirname, 'src'),
        path.resolve(__dirname, 'node_modules'),
    ],
  },
}