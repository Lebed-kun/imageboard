import React, { Component } from 'react';
import axios from 'axios';
import Router from 'next/router';
import { Input, Button, Form } from 'antd';

import HTTPForm from '../../../core/Form/Form.jsx';

import { BASE_REST_URL } from '../../../constants.js';

const Item = Form.Item;
const Password = Input.Password;

class LoginForm extends Component {
    handleRequest = values => {
        return axios.post(`${BASE_REST_URL}/user_post/authorize/`, values);
    }

    handleResponse = res => {
        const token = JSON.stringify(res.data);
        localStorage.setItem('token', token);
        Router.push('/');
    }
    
    render() {
        const getFieldDecorator = this.props.form.getFieldDecorator;

        return (
            <HTTPForm title="Вход" onRequest={this.handleRequest} onResponse={this.handleResponse}>
                <Item>
                    {getFieldDecorator('username', {
                        rules : [
                            {
                                required : true,
                                whitespace : true,
                                message : 'Введите логин/email!'
                            }
                        ]
                    })(<Input placeholder="Имя пользователя/email" />)}
                </Item>

                <Item>
                    {getFieldDecorator('password', {
                            rules : [
                                {
                                    required : true,
                                    whitespace : true,
                                    message : 'Введите пароль!'
                                }
                            ]
                    })(<Password placeholder="Пароль" />)}
                </Item>

                <Item>
                    <Button type="primary" htmlType="submit">
                        Войти
                    </Button>
                </Item>
            </HTTPForm>
        )
    }
}

export default Form.create({ name : 'login' })(LoginForm);