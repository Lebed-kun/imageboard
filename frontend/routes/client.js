import { Route, ClientRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOM from 'react-dom';
import { Pagination } from 'antd';
import { createStore } from 'redux';
import { Provider, connect } from 'react-redux';
import makeReducer from '../core/makeReducer/makeReducer.js';

import Menu from '../components/Menu/Menu.jsx';
import Form, { POST_FORM_MODES as formModes } from '../components/PostForm/PostForm.jsx';
import Thread, { THREAD_MODES } from '../components/Thread/Thread.jsx';

const router = ClientRouter(
    Route('/boards/:abbr', ({ abbr }) => {
        const THREADS_PER_PAGE = 10;
        const { menu, board, currentPage } = window.__PRELOADED_STATE__;
        
        ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu'));
        ReactDOM.hydrate(<Form boardAbbr={abbr} />, document.getElementById('form'));
        
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
    }),
    Route('/threads/:id', ({ id }) => {
        const { menu, thread, threadId } = window.__PRELOADED_STATE__;

        const store = createStore(makeReducer({
            'ADD_POST' : (state, action) => ({
                posts : state.posts.concat([action.payload])
            })
        }), {
            posts : thread
        });

        Form = connect(null, dispatch => ({
            addPost : post => dispatch({
                type: 'ADD_POST',
                payload: post
            })
        }))(Form);

        Thread = connect(state => ({
            data : state.posts
        }))(Thread);

        ReactDOM.hydrate(<Menu {...menu} />, document.getElementById('menu'));
        ReactDOM.hydrate((
            <Provider store={store}>
                <Form mode={formModes.CREATE_POST} threadId={threadId} />
            </Provider>
        ), document.getElementById('form'));
        ReactDOM.hydrate((
            <Provider store={store}>
                <Thread mode={THREAD_MODES.FULL_THREAD} />
            </Provider>
        ), document.getElementById('thread'));
    })
)

export default router;