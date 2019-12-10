const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./client.js",
  output: {
    path: path.join(__dirname, "/dist/"),
    filename: "app.js"
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        },
      },
      {
        test : /\.less|\.css$/,
        use : ['style-loader', 'css-loader', 'less-loader']
      }
    ]
  }
};