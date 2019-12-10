import express from "express";
import path from "path";

import React from "react";
import { renderToString } from "react-dom/server";

const server = express();
const port = process.env.PORT || 3000;

server.get('/boards/:abbr', (req, res) => {
    return app.render(req, res, '/boards', { abbr : req.params.abbr });
})

server.all('*', (req, res) => {
    return handle(req, res);
});

server.listen(port, err => {
    if (err) throw err;
    console.log(`Server is listening on port ${port}!`);
})