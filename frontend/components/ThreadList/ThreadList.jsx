import React from 'react';

import Thread from '../Thread/Thread.jsx';

/**
 * @typedef {import('../Thread/Thread.jsx')} Thread
 */

/**
 * 
 * @param {Object} param0
 * @property {Array<Thread>} data
 * @property {?[any]} store
 * 
 * @returns {React.ReactElement} 
 */
const ThreadList = ({ data }) => data.map((el, id) => (
    <Thread 
        key={id}
        data={el}
    />
))

export default ThreadList;