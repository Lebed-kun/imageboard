import axios from 'axios';
import { message } from 'antd';
import filter from '../../core/ObjectUtils/filter.js';

import { BASE_REST_URL } from '../../config.js';

/**
 * 
 * @param {string} reason
 * @returns {(dispatch, getState) => any} 
 */
const reportPosts = reason => async (dispatch, getState) => {
    try {
        await axios.post(`${BASE_REST_URL}/main_post/threads/0/report/`, {
            reason,
            ids : Object.keys(filter(getState().selectedPosts, val => val))
        });

        message.success('Жалоба отправлена!');
        setTimeout(() => dispatch({
            type : 'REPORT_SUCCESS'
        }), 2000);
    } catch (err) {
        console.log(err);
        message.err(err);
        setTimeout(() => dispatch({
            type : 'REPORT_FAIL'
        }), 2000);
    }
}

export default reportPosts;