import { Route, ClientRouter } from '../core/Router/index.js';
import React from 'react';
import ReactDOM from 'react-dom';
import { Pagination } from 'antd';
import { createStore } from 'redux';
import { Provider, connect } from 'react-redux';
import makeReducer from '../core/makeReducer/makeReducer.js';
import { connectNodes } from '../core/connectNodes/connectNodes.js';

import Menu from '../components/Menu/Menu.jsx';
import PostForm, { POST_FORM_MODES as formModes } from '../components/PostForm/PostForm.jsx';
import Thread from '../components/Thread/Thread.jsx';
import THREAD_MODES from '../components/Thread/thread_modes.js';

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

        connectNodes(
            { idProp : 'id', textProp : 'message', linkProp : 'responses' }, 
            /(?<=>>)[0-9]+/g
        )(thread);

        const store = createStore(makeReducer({
            'ADD_POST' : (state, action) => ({
                ...state,
                posts : state.posts.concat([action.payload])
            }),
            'APPEND_POST_LINK' : (state, action) => ({
                ...state,
                newPostLink : action.payload
            })
        }), {
            posts : thread,
            newPostLink : ''
        });

        const WrapPostForm = connect(state => ({
            newPostLink : state.newPostLink
        }), dispatch => ({
            addPost : post => dispatch({
                type: 'ADD_POST',
                payload: post
            })
        }))(PostForm);

        const WrapThread = connect(state => ({
            data : state.posts
        }), dispatch => ({
            appendLink : postId => dispatch({
                type: 'APPEND_POST_LINK',
                payload: `>>${postId}`
            })
        }))(Thread);

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