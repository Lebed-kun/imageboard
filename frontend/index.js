require("@babel/register")({
    presets: ["@babel/preset-env", '@babel/preset-react'],
    plugins: ["@babel/plugin-proposal-class-properties", '@babel/plugin-transform-runtime']
});
  
module.exports = require("./server.js");