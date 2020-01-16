import React, { Component } from 'react';
import { Form, Button, message } from 'antd';
import axios from 'axios';

import HTTPForm from '../../../core/Form/Form.jsx';
import RichText from '../../../core/RichText/RichText.jsx';

import { BASE_REST_URL } from '../../../constants.js';

class ReportForm extends Component {
    static MAX_REASON_LENGTH = 200;

    handleRequest = values => {
        const ids = [this.props.postId];
        const url = `${BASE_REST_URL}/main_post/threads/${this.props.threadId}/report/`
        return axios.post(url, {
            ids : ids,
            reason : values.reason
        });
    }

    handleResponse = () => {
        message.success('Жалоба успешно отправлена!');
    }

    handleError = err => {
        message.error(err);
        console.log(err);
    }

    richTextDecorator = component => {
        const { getFieldDecorator } = this.props.form;
        
            return getFieldDecorator('reason', {
                initialValue : '',
                rules : [
                    {
                        required : true,
                        whitespace : true,
                        max : ReportForm.MAX_REASON_LENGTH
                    }
                ]
            })(component)
    }

    initProps = {
        form : this.props.form,
        onRequest : this.handleRequest,
        onResponse : this.handleResponse,
        onError : this.handleError
    }
    
    render() {
        return (
            <HTTPForm {...this.initProps}>
                <RichText 
                    fieldDecorator={this.richTextDecorator}
                    maxCount={ReportForm.MAX_REASON_LENGTH}
                />

                <Button type="primary" htmlType="submit">
                    Отправить
                </Button>
            </HTTPForm>
        )
    }
}

ReportForm = Form.create({ name : 'report' })(ReportForm);

export default ReportForm;