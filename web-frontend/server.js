const express = require('express');
const next = require('next');

const port = +process.env.PORT || 3000;
const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
    const server = express();

    server.get('/boards/:abbr', (req, res) => {
        const query = {
            abbr : req.params.abbr,
            page : req.query.page
        }
        return app.render(req, res, '/boards', query);
    })

    server.all('*', (req, res) => {
        return handle(req, res);
    });

    server.listen(port, err => {
        if (err) throw err;
        console.log(`Server is listening on port ${port}!`);
    })
});