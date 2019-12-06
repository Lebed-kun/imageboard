import React, { Component } from 'react';
import { Form, Card } from 'antd';

class HttpForm extends Component {
    state = {
        error : null
    }

    handleSubmit = e => {
        e.preventDefault();

        this.props.form.validateFields((err, values) => {
            if (!err) {
                const handleRequest = this.props.onRequest;
                handleRequest(values).then(res => {
                    const handleResponse = this.props.onResponse;
                    return handleResponse(res);
                })
                .catch(err => {
                    console.log(err);
                    this.setState({
                        error : err.message
                    })
                })
            }
        })
    }

    getErrorComponent = () => {
        const message = this.state.error;
        return message ? <p>{message}</p> : null;
    }
    
    render() {
        return (
            <Card title={this.props.title}>
                {this.getErrorComponent()}

                <Form onSubmit={this.handleSubmit}>
                    {this.props.children}
                </Form>
            </Card>
        )
    }
}

export default HttpForm;