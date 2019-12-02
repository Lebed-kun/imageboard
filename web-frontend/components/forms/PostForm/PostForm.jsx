import React, { Component } from 'react';
import axios from 'axios';
import Router from 'next/router';
import { Input, Button, Form, Checkbox, Row, Col, Upload } from 'antd';

import HTTPForm from '../../../core/Form/Form.jsx';
import RichText from '../../../core/RichText/RichText.jsx';

import tags from '../../../bb_tags/tags.js';

import { BASE_REST_URL, EMAIL_REGEX, URL_REGEX } from '../../../constants.js';

const { Item } = Form;
const { Dragger } = Upload;

class PostForm extends Component {
    static MAX_MESSAGE_LENGTH = 15000;
    
    getButtonTitle = () => {
        const thread = this.props.thread;
        return !thread ? 'Создать' : 'Отправить';
    }

    validateContact = (rule, value, next) => {
        if (!value) {
            next();
            return;
        }
        
        const matchesEmail = value.match(EMAIL_REGEX);
        if (matchesEmail) {
            next();
            return;
        }

        const matchesUrl = value.match(URL_REGEX);
        if (matchesUrl) {
            next();
            return;
        }

        next(true);
    }

    richTextDecorator = component => {
        const { getFieldDecorator } = this.props.form;
        
            return getFieldDecorator('message', {
                initialValue : '',
                rules : [
                    {
                        required : true,
                        whitespace : true,
                        max : PostForm.MAX_MESSAGE_LENGTH
                    }
                ]
            })(component)
    }

    setRichTextValue = tag => {
        const { setFieldsValue, getFieldValue } = this.props.form;
        const value = getFieldValue('message');
        setFieldsValue({ message : value + tag });
    }

    handleRequest = values => {
        let url = `${BASE_REST_URL}/main_post/`;
        
        const thread = this.props.thread;
        const board = this.props.board;
        if (thread) {
            url += `threads/${thread}/create/`
        } else {
            url += `boards/${board}/create/`
        }

        return axios.post(url, values);
    }

    // TO DO : rich text field
    render() {
        const { getFieldDecorator, getFieldValue } = this.props.form;

        return (
            <HTTPForm onRequest={this.handleRequest}>
                <Row key="1">
                    <Col key="title">
                        <Item>
                            {getFieldDecorator('title')(
                                <Input placeholder="Заголовок" />
                            )}
                        </Item>
                    </Col>

                    <Col key="submit">
                        <Item>
                            <Button type="primary" htmlType="submit">
                                {this.getButtonTitle()}
                            </Button>
                        </Item>
                    </Col>
                </Row>

                <Row key="2">
                    <Col key="author" span={12}>
                        <Item>
                            {getFieldDecorator('author')(
                                <Input placeholder="Автор" />
                            )}
                        </Item>
                    </Col>

                    <Col key="contact" span={12}>
                        <Item>
                            {getFieldDecorator('contact', {
                                rules : [
                                    {
                                        message : 'Можно указать email или сайт!',
                                        validator : this.validateContact
                                    }
                                ]
                            })(<Input placeholder="Email/Сайт"/>)}
                        </Item>
                    </Col>
                </Row>

                <Item key="options">
                    {getFieldDecorator('options[0]')(
                        <Checkbox>
                            Sage
                        </Checkbox>
                    )}
                </Item>

                <Item key="message">
                    <RichText
                        fieldDecorator={this.richTextDecorator}
                        setValue={this.setRichTextValue}
                        tags={tags}
                        maxCount={PostForm.MAX_MESSAGE_LENGTH}
                    />
                </Item>

                <Item key="files">
                    {getFieldDecorator('files')(
                        <Dragger name="files" multiple={true}>
                            ДОБАВЬТЕ СЮДА ФАЙЛЫ (не более 5 МБ общим весом, не более 4-х)
                        </Dragger>
                    )}
                </Item>
            </HTTPForm>
        )
    }
}

export default Form.create({ name : 'create_post' })(PostForm);