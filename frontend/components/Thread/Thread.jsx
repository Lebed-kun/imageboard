import React from 'react';

import Post from '../Post/Post.jsx';
import THREAD_MODES from './thread_modes.js';

/**
 * @typedef {import('../Post/Post.jsx')} Post
 */

/**
 * @typedef {Object} Thread
 * @property {number} id
 * @property {boolean} sticked
 * @property {boolean} read_only
 * @property {Post} first_post 
 * @property {Array<Post>} last_posts 
 */

/**
 * 
 * @param {Object} param0 
 * @property {Thread|Array<Post>} data
 * @property {postId : number => void} appendLink
 * @property {?string} mode
 * @property {...any} props
 * 
 * @returns {React.ReactElement}
 */
const Thread = ({ data, threadId, mode = THREAD_MODES.DEFAULT_THREAD, appendLink, ...props }) => (
    <div {...props}>
        {mode === THREAD_MODES.DEFAULT_THREAD && (
            <>
                <Post
                    key={0} 
                    data={data.first_post}
                    threadId={data.id}
                    sticked={data.sticked}
                    threadMode={mode}
                />

                {!!data.last_posts.length && (
                    <>
                        <p>Показано {data.last_posts.length} последних постов</p>
                        {data.last_posts.map((_, id, posts) => (
                            <Post 
                                key={id + 1}
                                data={posts[posts.length - 1 - id]}
                                threadId={data.id}
                                threadMode={mode}
                            />
                        ))}
                    </>
                )}
            </>
        )}

        {mode === THREAD_MODES.FULL_THREAD && data.map((el, id) => (
            <Post 
                key={id}
                data={el}
                threadId={threadId}
                sticked={id === 0 && data.sticked}
                threadMode={mode}
                appendLink={appendLink}
            />
        ))}
    </div>
)

export default Thread;