import { Route, ClientRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOM from 'react-dom';
import { Pagination } from 'antd';
import { createStore } from 'redux';
import { Provider, connect } from 'react-redux';
import makeReducer from '../core/makeReducer/makeReducer.js';

import Menu from '../components/Menu/Menu.jsx';
import PostForm, { POST_FORM_MODES as formModes } from '../components/PostForm/PostForm.jsx';
import Thread, { THREAD_MODES } from '../components/Thread/Thread.jsx';

const router = ClientRouter(
    Route('/boards/:abbr', ({ abbr }) => {
        const THREADS_PER_PAGE = 10;
        const { menu, board, currentPage } = window.__PRELOADED_STATE__;
        
        setTimeout(() => ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu')));
        setTimeout(() => ReactDOM.hydrate(<PostForm boardAbbr={abbr} />, document.getElementById('form')));
        
        if (board.pages_count > 1) {
            setTimeout(() => ReactDOM.hydrate((
                <Pagination 
                    total={board.pages_count * THREADS_PER_PAGE}
                    pageSize={THREADS_PER_PAGE}
                    current={currentPage}
                    onChange={page => window.location.href = `/boards/${abbr}?page=${page}`}
                />
            ), document.getElementById('pagination')));
        }
    }),
    Route('/threads/:id', () => {
        const { menu, thread, threadId } = window.__PRELOADED_STATE__;

        const store = createStore(makeReducer({
            'ADD_POST' : (state, action) => ({
                posts : state.posts.concat([action.payload])
            })
        }), {
            posts : thread
        });

        const WrapPostForm = connect(null, dispatch => ({
            addPost : post => dispatch({
                type: 'ADD_POST',
                payload: post
            })
        }))(PostForm);

        const WrapThread = connect(state => ({
            data : state.posts
        }), null)(Thread);

        setTimeout(() => ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu')));
        setTimeout(() => ReactDOM.hydrate((
            <Provider store={store}>
                <WrapPostForm mode={formModes.CREATE_POST} threadId={threadId} />
            </Provider>
        ), document.getElementById('form')));
        setTimeout(() => ReactDOM.hydrate((
            <Provider store={store}>
                <WrapThread mode={THREAD_MODES.FULL_THREAD} threadId={threadId} />
            </Provider>
        ), document.getElementById('thread')));
    })
)

export default router;