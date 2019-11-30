import React, { Component } from 'react';
import axios from 'axios';
import Router from 'next/router';
import { Input, Button, Form, Row } from 'antd';

import HTTPForm from '../../../core/Form/Form.jsx';

import { BASE_REST_URL } from '../../../constants.js';

const Item = Form.Item;

class PostForm extends Component {
    render() {
        return (
            <HTTPForm>

            </HTTPForm>
        )
    }
}

export default Form.create({ name : 'create_post' })(PostForm);