import { Route, Router as ServerRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOMServer from 'react-dom/server';
import fs from 'fs';

import Page from '../pages/base.js';
import Board from '../pages/Board/Board.jsx';

const router = ServerRouter(
    Route('/', (params, query, { res }) => res.redirect('/boards/lrk')),
    Route('/static/*', (params, query, { req, res }) => {
        fs.readFile(__dirname + req.url, 'utf-8', (err, data) => {
            res.setHeader('Content-type', 'application/javascript');
            res.write(data);
            res.end();
        })
    }, true),
    Route('/boards/:abbr', async ({ abbr }, query, { res }) => {
        const initProps = await Board.getInitialProps({ abbr });
        const page = Page(`/${abbr}/`, ReactDOMServer.renderToString(<Board {...initProps}/>), {
            menu : initProps
        });
        res.write(page);
        res.end();
    }, true)
)

export default router;
