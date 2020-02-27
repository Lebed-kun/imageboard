import { Route, ClientRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOM from 'react-dom';
import { Pagination } from 'antd';

import Menu from '../components/Menu/Menu.jsx';

const router = ClientRouter(
    Route('/boards/:abbr', ({ abbr }) => {
        const THREADS_PER_PAGE = 10;
        const { menu, board, currentPage } = window.__PRELOADED_STATE__;
        
        ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu'));
        
        if (board.pages_count > 1) {
            ReactDOM.hydrate((
                <Pagination 
                    total={board.pages_count * THREADS_PER_PAGE}
                    pageSize={THREADS_PER_PAGE}
                    current={currentPage}
                    onChange={page => window.location.href = `/boards/${abbr}?page=${page}`}
                />
            ), document.getElementById('pagination'));
        }
    })
)

export default router;