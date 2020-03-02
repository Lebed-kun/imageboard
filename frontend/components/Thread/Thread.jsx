import React from 'react';

import Post from '../Post/Post.jsx';

/**
 * @typedef {import('../Post/Post.jsx')} Post
 */

export const THREAD_MODES = {
    DEFAULT_THREAD : 'DEFAULT_THREAD', // Thread with first and last posts
    FULL_THREAD : 'FULL_THREAD' // Thread with all its posts
}

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
 * @property {?string} mode
 * @property {...any} props
 * 
 * @returns {React.ReactElement}
 */
const Thread = ({ data, threadId, mode = THREAD_MODES.DEFAULT_THREAD, ...props }) => (
    <div {...props}>
        {mode === THREAD_MODES.DEFAULT_THREAD && (
            <>
                <Post
                    key={0} 
                    data={data.first_post}
                    threadId={data.id}
                    sticked={data.sticked}
                />

                {!!data.last_posts.length && (
                    <>
                        <p>Показано {data.last_posts.length} последних постов</p>
                        {data.last_posts.map((_, id, posts) => (
                            <Post 
                                key={id + 1}
                                data={posts[posts.length - 1 - id]}
                                threadId={data.id}
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
            />
        ))}
    </div>
)

export default Thread;