import React, { Component } from 'react';
import axios from 'axios';
import Router from 'next/router';
import { Input, Button, Form, Checkbox, Row, Col } from 'antd';

import HTTPForm from '../../../core/Form/Form.jsx';

import { BASE_REST_URL, EMAIL_REGEX, URL_REGEX } from '../../../constants.js';

const Item = Form.Item;

class PostForm extends Component {
    getButtonTitle = () => {
        const thread = this.props.thread;
        return !thread ? 'Создать' : 'Отправить';
    }

    validateContact = (rule, value, next) => {
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
        const getFieldDecorator = this.props.form.getFieldDecorator;

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
            </HTTPForm>
        )
    }
}

export default Form.create({ name : 'create_post' })(PostForm);