import React from 'react';
import { Card, Button } from 'antd';

import { BASE_BACKEND_URL } from '../../config.js';
import THREAD_MODES from '../Thread/thread_modes.js';

const hElementStyle = {
    display : 'inline-block'
}

/**
 * @typedef {Object} File
 * @property {string} name
 * @property {string} url
 * 
 * @typedef {Object} Post
 * @property {number} id 
 * @property {string} title
 * @property {?string} author
 * @property {?string} contact
 * @property {?string} options
 * @property {string} message
 * @property {string} created_at
 * @property {string} updated_at
 * @property {Array<File>} files  
 */

/**
 * @param {Post} data
 * @returns {string} 
 */
const getAuthor = data => data.author || 'Аноним';

const EMAIL_REGEX = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
/**
 * 
 * @param {string} contact
 * @returns {boolean} 
 */
const isEmail = contact => EMAIL_REGEX.test(contact);

/**
 * 
 * @param {string} threadMode 
 * @param {number} postId 
 * @param {?number} threadId
 * @returns {string} 
 */
const postLink = (threadMode, postId, threadId) => `${threadMode === THREAD_MODES.DEFAULT_THREAD ? `/threads/${threadId}` : ''}#${postId}`;

/**
 * @param {Object} param0
 * @property {Post} data 
 * @property {number} threadId
 * @property {boolean} sticked
 * @property {Array<number>} responses
 * @property {...any} props
 * 
 * @returns {React.ReactElement}
 */
const Post = ({ data, threadId, threadMode, sticked, ...props }) => (
    <Card id={data.id} {...props}>
        <div>
            <h3 style={hElementStyle}>{data.title}</h3>
            от
            <p style={hElementStyle}>
                {
                    data.contact ? (
                        <a href={isEmail(data.contact) ? `mailto:${data.contact}` : data.contact}>
                            {getAuthor(data)}
                        </a>
                    ) : getAuthor(data)
                }
            </p>

            <a href={postLink(threadMode, data.id, threadId)}>
                #{data.id}
            </a>
        </div>

        <div>
            {!!data.options && `
                    Опции: 
                    ${data.options.split(',').join(', ')}
                `
            }

            {data.created_at}
        </div>

        <div key="files">
            {!!data.files && data.files.map((el, id) => (
                <Card key={id} style={hElementStyle}>
                    <img src={`${BASE_BACKEND_URL}${el.url}`} width="200" height="200" />
                    <p>{el.name}</p>
                </Card>
            ))}
        </div>

        <p>
            {data.message}
        </p>

        {!!data.responses && (
            <div key="responses">
                Ответы: 
                {data.responses.map((el, id) => (
                    <a key={id} href={postLink(threadMode, el, threadId)}>
                        {`>>${el}`}
                    </a>
                ))}
            </div>
        )}
    </Card>
)

export default Post;
