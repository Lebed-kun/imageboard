import React from 'react';
import axios from 'axios';
import { Form, Input, Checkbox, Upload, Button, Row, Col } from 'antd'

import { BASE_REST_URL } from '../../config.js';

const POST_FORM_MODES = {
    CREATE_THREAD : (boardAbbr, data) => axios.post(`${BASE_REST_URL}/main_post/boards/${boardAbbr}/create/`, data),
    CREATE_POST : (threadId, data) => axios.post(`${BASE_REST_URL}/main_post/threads/${threadId}/create/`, data)
};

const EMAIL_REGEX = /^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/;
const URL_REGEX = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;

/**
 * @param {Object} param0
 * @property {*} form
 * @property {Function} mode
 * @property {number} threadId
 * @property {...any} props
 * 
 * @returns {React.ReactElement} 
 */
const PostForm = ({ form, mode = POST_FORM_MODES.CREATE_THREAD, threadId, ...props }) => {
    
    
    return (
        <Form>
            <Form.Item name="title">
                <Input 
                    name="title"
                    placeholder="Название треда"
                />
            </Form.Item>

            <Row>
                <Form.Item name="author">
                    <Input 
                        name="author"
                        placeholder="Имя"
                    />
                </Form.Item>

                <Form.Item
                    name="contact"
                    rules={[
                        {
                            validator : (rule, value) => {
                                if (!value.length || value.match(EMAIL_REGEX) || value.match(URL_REGEX)) {
                                    return Promise.resolve();
                                }
                                return Promise.reject("Некорректный email или сайт!")
                            },
                            message: "Некорректный email или сайт"
                        }
                    ]}
                >
                    <Input 
                        name="contact"
                        placeholder="Email/Сайт"
                    />
                </Form.Item>
            </Row>

            <Row>
                Опции:
                <Form.Item name="options">
                    <Checkbox.Group>
                        <Checkbox value="sage">Sage</Checkbox>
                    </Checkbox.Group>
                </Form.Item>
            </Row>

            <Form.Item name="message" rules={[
                {
                    required: true,
                    whitespace: true
                }
            ]}>
                <Input.TextArea name="message" placeholder="Тексто сообщения" />
            </Form.Item>
        </Form>
    );
};

export default Form.create({ name : 'post_form' })(PostForm);