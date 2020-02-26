import { Route, ClientRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOM from 'react-dom';

import Menu from '../components/Menu/Menu.jsx';

const router = ClientRouter(
    Route('/boards/:abbr', ({ abbr }) => {
        const { menu } = window.__PLELOADED_STATE__;
        ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu'));
    })
)

export default router;