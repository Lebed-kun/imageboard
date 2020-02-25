const path = require("path");

module.exports = {
  entry: "./client.js",
  output: {
    path: path.join(__dirname, "/static/js/"),
    filename: "client.js"
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options : {
            presets: [
              "@babel/preset-env",
              "@babel/preset-react"
            ],
            plugins: [
                "@babel/plugin-proposal-class-properties"
            ]
          }
        },
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
};