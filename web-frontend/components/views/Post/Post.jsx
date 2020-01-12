import React, { Component } from 'react';
import { Card, Row, Button } from 'antd';
import Parser from '../../../bb_tags/register.js';

import Preview from '../../../core/Preview/Preview.jsx';

import { BASE_URL } from '../../../constants.js';

class Post extends Component {
    prepareOptions = options => {
        return options.replace(',', ' ');
    }

    prepareFiles = files => {
        if (!files || !files.length) return null;

        return files.map((el, id) => (
            <Preview 
                key={id}
                name={el.name}
                url={`${BASE_URL}${el.url}`}
            />
        ))
    }
    
    card = () => {
        const data = this.props.data;
        const uid = this.props.uid;
        const threadId = this.props.threadId;
        const options = this.prepareOptions(data.options);
        const files = this.prepareFiles(data.files);

        return (
            <Card>
                <Row key="heading">
                    <h3>{data.title.replace(/\[.+\]/g, '')}</h3>

                    <Button href={`/threads/${threadId}`}>
                        Ответить
                    </Button>
                </Row>

                <Row key="subheading">
                    <a href={data.contact || null}>
                        {data.author || 'Аноним'}
                    </a>

                    <p key="created_at">Создан: {data.created_at}</p>

                    <p key="updated_at">Изменен: {data.updated_at}</p>

                    <p key="uid">{uid}</p>

                    <p key="id">{data.id}</p>

                    <Button>
                        Жалоба
                    </Button>

                    <Button>
                        Скрыть
                    </Button>
                </Row>

                <Row key="options">
                    Опции:
                    {options}
                </Row>

                <Row key="body">
                    {files}

                    <p>
                        {Parser.toReact(
                            data.message
                        )}
                    </p>
                </Row>
            </Card>
        )
    }
    
    render() {
        return this.card();
    }
}

export default Post;