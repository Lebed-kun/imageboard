import React, { Component } from 'react';
import { Form } from 'antd';

class HttpForm extends Component {
    // TODO : handle error
    
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

    initProps = {
        onSubmit : this.handleSubmit,
        mode : this.props.mode || 'horizontal'
    }
    
    render() {
        return (
            <Form {...this.initProps}>
                {this.getErrorComponent()}

                {this.props.children}
            </Form>
        )
    }
}

export default HttpForm;