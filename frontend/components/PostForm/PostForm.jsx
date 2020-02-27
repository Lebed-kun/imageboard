import React from 'react';
import axios from 'axios';
import { Form, Input, Checkbox, Upload, Button } from 'antd'

import { BASE_REST_URL } from '../../config.js';

const POST_FORM_MODES = {
    CREATE_THREAD : (boardAbbr, data) => axios.post(`${BASE_REST_URL}/api/main_post/boards/${boardAbbr}/create/`, data),
    CREATE_POST : (threadId, data) => axios.post(`${BASE_REST_URL}/api/main_post/threads/${threadId}/create/`, data)
}

const PostForm = ({ form }) => {};

export default Form.create()(PostForm);