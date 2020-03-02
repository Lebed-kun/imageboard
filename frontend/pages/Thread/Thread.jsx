import React from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../config.js';

import Menu from '../../components/Menu/Menu.jsx';
import Form, { POST_FORM_MODES as formModes } from '../../components/PostForm/PostForm.jsx';
import ThreadView, { THREAD_MODES } from '../../components/Thread/Thread.jsx';

const Thread = ({ menu, thread, threadId }) => {
    <>
        <div id="menu">
            <Menu {...menu}/>
        </div>

        <div id="form">
            <Form mode={formModes.CREATE_POST} threadId={threadId} />
        </div>

        <div id="thread">
            <ThreadView mode={THREAD_MODES.FULL_THREAD} data={thread} />
        </div>
    </>
}

Thread.getInitialProps = async ({ threadId }) => {
    try {
        const boardsRes = await axios.get(`${BASE_REST_URL}/main_get/`);
        const threadRes = await axios.get(`${BASE_REST_URL}/main_get/threads/${threadId}/`);
        return {
            menu : { boards : boardsRes.data, userboardService : {
                key : 'userboards',
                link : '/userboards/',
                title : 'Юзердоски'
            }, support : {
                key : 'support',
                link : '/support/',
                title : 'Поддержка'
            }, currentLink : `/boards/${abbr}`},
            thread : threadRes.data,
            threadId
        };
    } catch (err) {
        console.log(err);
        return {};
    }
}

export default Thread;