import { Route, Router as ServerRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOMServer from 'react-dom/server';
import fs from 'fs';
import path from 'path';

import Page from '../pages/base.js';
import Board from '../pages/Board/Board.jsx';
import Thread from '../pages/Thread/Thread.jsx';

const router = ServerRouter(
    /* Route('/', (params, query, { req, res }) => {
        res.writeHead(301, {
            Location : `http${req.socket.encrypted ? 's' : ''}://${req.headers.host}/boards/lrk`
        });
    }), */
    Route('/static/*', (params, query, { req, res }) => {
        fs.readFile(path.join(__dirname, `../${req.url.slice(1)}`), 'utf-8', (err, data) => {
            res.write(data);
            res.end();
        })
    }, true),
    Route('/boards/:abbr', ({ abbr }, { page }, { res }) => {
        Board.getInitialProps({ abbr, page }).then(initProps => {
            const page = Page(`/${initProps.board.board.abbr}/ - ${initProps.board.board.name}`, ReactDOMServer.renderToString(<Board {...initProps}/>), initProps);
            res.write(page);
            res.end();
        });
    }, true),
    Route('/threads/:id', ({ id }, q, { res }) => {
        Thread.getInitialProps({ threadId : id }).then(initProps => {
            const page = Page(initProps.thread[0].title, ReactDOMServer.renderToString(<Thread {...initProps}/>), initProps);
            res.write(page);
            res.end();
        })
    })
)

export default router;
