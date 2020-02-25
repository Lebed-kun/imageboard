import { Route, Router as ServerRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOMServer from 'react-dom/server';

import Board from '../pages/Board/Board.jsx';

const router = ServerRouter(
    Route('/boards/:abbr', async ({ abbr }) => {
        const initProps = await Board.getInitialProps({ abbr });
        return ReactDOMServer.renderToString(<Board {...initProps} />)
    }, true)
)

export default router;
