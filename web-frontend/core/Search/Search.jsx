import React, { Component } from 'react';
import { Input, Select, Button, Form } from 'antd';

import HttpForm from '../Form/Form.jsx';

const { Option } = Select;

class Search extends Component {
    handleRequest = values => {
        const searchUrl = this.props.searchUrl;
        const query = values.query;

        let fields = values.fields;
        if (fields) {
            fields = fields.join(',');
        }
        
        let url = `${searchUrl}?q=${query}`; 
        url = url + `${fields ? `&fields=${fields}` : ''}`;

        return this.props.onRequest(url);
    }

    getFilters = () => {
        const { getFieldDecorator } = this.props.form;
        const fields = this.props.fields;

        if (!fields) return null;

        return (
            <Form.Item key="fields">
                {getFieldDecorator('fields')(
                    <Select mode="multiple" placeholder="Искать в">
                        {fields.map((el, id) => (
                            <Option key={id} value={el.value}>
                                {el.title}
                            </Option>
                        ))}
                    </Select>
                )}
            </Form.Item>
        )
    }

    initProps = {
        form : this.props.form,
        onRequest : this.handleRequest,
        onResponse : this.props.onResponse,
        mode : 'inline'
    }
    
    render() {
        const { getFieldDecorator } = this.props.form;

        return (
            <HttpForm {...this.initProps}>
                <Form.Item key="query">
                    {getFieldDecorator('query')(<Input placeholder="Поиск..." />)}
                </Form.Item>

                {this.getFilters()}

                <Form.Item key="submit">
                    <Button type="primary" htmlType="submit">
                        Искать
                    </Button>
                </Form.Item>
            </HttpForm>
        )
    }
}

const SearchWrapper = name => {
    return Form.create({ name : `${name}_search` })(Search);
}

export default SearchWrapper;