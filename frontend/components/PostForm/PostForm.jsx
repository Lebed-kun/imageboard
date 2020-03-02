import React from 'react';
import axios from 'axios';
import { Form, Input, Checkbox, Upload, Button, Row, Col, message } from 'antd'

import { BASE_REST_URL } from '../../config.js';

const { Dragger } = Upload;

export const POST_FORM_MODES = {
    CREATE_THREAD : (boardAbbr, data) => axios.post(`${BASE_REST_URL}/main_post/boards/${boardAbbr}/create/`, data),
    CREATE_POST : (threadId, data) => axios.post(`${BASE_REST_URL}/main_post/threads/${threadId}/create/`, data)
};

const EMAIL_REGEX = /^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/;
const URL_REGEX = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/;

const normFiles = e => {
    return Array.isArray(e) ? e : e && e.fileList;
}

const prepareFiles = values => {
    const files = values.files.map(el => ({
        name : el.name,
        content : el.content
    }));
    values.files = files;
}

const prepareOptions = values => {
    if (!values.options) return;
    values.options = values.options.join(',');
}

const beforeUpload = file => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = e => {
            file.content = e.target.result;
            resolve(file);
        };

        reader.onerror = e => {
            console.log(e.target.error);
            reject(e.target.error);
        }
    })
}

/**
 * @param {Object} param0
 * @property {*} form
 * @property {Function} mode
 * @property {number} threadId
 * @property {...any} props
 * 
 * @returns {React.ReactElement} 
 */
const PostForm = ({ form, mode = POST_FORM_MODES.CREATE_THREAD, boardAbbr, threadId, addPost, ...props }) => {
    const formProps = () => ({
        name : 'post',
        initialValues : {
            email : '',
            message : '',
            files : []
        },
        onFinish: async values => {
            prepareOptions(values);
            prepareFiles(values);

            try {
                const response = await mode(threadId || boardAbbr, values);
                if (boardAbbr) {
                    message.success(`Тред #${response.data.id} успешно создан!`);
                    setTimeout(() => window.location.href = `/threads/${response.data.id}`, 2000);
                } else {
                    addPost(response.data);
                }
            } catch (err) {
                message.error(err);
                console.log(err);
            }
        }
    })
    
    return (
        <Form {...formProps()} {...props}>
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

                <Form.Item name="options" label="Опции:">
                    <Checkbox.Group name="options">
                        <Checkbox value="sage">Sage</Checkbox>
                    </Checkbox.Group>
                </Form.Item>

            <Form.Item name="message" rules={[
                {
                    required: true,
                    whitespace: true,
                    message: 'Введите сообщение!'
                }
            ]}>
                <Input.TextArea name="message" placeholder="Текст сообщения" />
            </Form.Item>

            <Form.Item name="files" valuePropName="fileList" getValueFromEvent={normFiles}>
                <Dragger 
                    multiple={true}
                    beforeUpload={beforeUpload}
                    customRequest={({file, onSuccess}) => setTimeout(() => onSuccess('ok'))}
                    listType="picture-card"
                >
                    ДЛЯ ЗАГРУЗКИ ФАЙЛОВ (не более 4-х, не более 5 МБ)
                </Dragger>
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit">
                    {mode === POST_FORM_MODES.CREATE_THREAD ? 'Создать' : 'Отправить'}
                </Button>
            </Form.Item>
        </Form>
    );
};

export default PostForm;