require("@babel/register")({
    presets: ["@babel/preset-env", '@babel/preset-react'],
    plugins: ["@babel/plugin-proposal-class-properties"]
});
  
module.exports = require("./server.js");