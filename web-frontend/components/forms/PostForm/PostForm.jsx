import React, { Component } from 'react';
import axios from 'axios';
import Router from 'next/router';
import { Input, Button, Form, Checkbox, Row, Col, message } from 'antd';
import { connect } from 'react-redux';

import HTTPForm from '../../../core/Form/Form.jsx';
import RichText from '../../../core/RichText/RichText.jsx';
import Upload from '../../../core/Uploader/Uploader.jsx';

import tags from '../../../bb_tags/tags.js';

import { BASE_REST_URL, EMAIL_REGEX, URL_REGEX } from '../../../constants.js';

import { changePosts } from '../../../store/actions/actions.js';

const { Item } = Form;

const mapStateToProps = state => {
    return {
        posts : state.posts
    }
}

const mapDispatchToProps = dispatch => {
    return {
        changePosts : posts => dispatch(changePosts(posts))
    }
}

class PostForm extends Component {
    // TODO : hide form

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

    uploadDecorator = component => {
        const { getFieldDecorator } = this.props.form;
        
        return getFieldDecorator('files', {
            valuePropName : 'fileList',
            getValueFromEvent : this.normFile
        })(component);
    }

    normFile = e => {
        if (Array.isArray(e)) {
            return e;
        }

        return e && e.fileList;
    }

    setRichTextValue = tag => {
        const { setFieldsValue, getFieldValue } = this.props.form;
        const value = getFieldValue('message');
        setFieldsValue({ message : value + tag });
    }

    prepareOptions = values => {
        if (!values.options) return;

        const { getFieldValue } = this.props.form;
        
        let options = getFieldValue('options');
        options = options.join(',');

        values.options = options;
    }

    prepareFiles = values => {
        const files = values.files.map(el => {
            return {
                name : el.name,
                content : el.content
            }
        });
        values.files = files;
    }

    handleRequest = values => {
        this.prepareOptions(values);
        
        if (values.files && values.files.length) {
            this.prepareFiles(values);
        }
        
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

    handleResponse = response => {
        const data = response.data;

        const thread = this.props.thread;
        const board = this.props.board;

        if (thread) {
            const posts = this.props.posts;
            const newPosts = posts.concat([data])
            this.props.changePosts(newPosts);

            message.success(`Сообщение успешно отправлено!`)
        } else {
            message.success(`Тред #${data.id} создан!`);
            setTimeout(() => {
                Router.push(`/threads/${data.id}/`)
            }, 1000);
        }
    }

    handleError = err => {
        message.error(err);
    }

    initProps = {
        form : this.props.form,
        onRequest : this.handleRequest,
        onResponse : this.handleResponse,
        onError : this.handleError
    }

    // TO DO : rich text field
    render() {
        const { getFieldDecorator, getFieldValue } = this.props.form;

        return (
            <HTTPForm {...this.initProps}>
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
                    {getFieldDecorator('options')(
                        <Checkbox.Group>
                            <Checkbox value="sage">
                                Sage
                            </Checkbox>
                        </Checkbox.Group>
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
                    <Upload 
                        fieldDecorator={this.uploadDecorator}
                        accept=".jpg,.jpeg,.png,.gif,.mp4,.webm,.mp3,.ogg,.pdf,.djvu" 
                    />
                </Item>
            </HTTPForm>
        )
    }
}

PostForm = Form.create({ name : 'create_post '})(PostForm);

export default connect(mapStateToProps, mapDispatchToProps)(PostForm);