import React, { Component } from 'react';

import Post from '../Post/Post.jsx'; 

class Thread extends Component {
    static COLUMN = 'column';
    static CARD = 'card';
    static FULL_COLUMN = 'full';
    
    columnThread = () => {
        const data = this.props.data;
        const firstPost = data.first_post;
        const lastPosts = data.last_posts.sort((a, b) => a.id - b.id);
        
        const style = {
            borderTop : '2px black solid',
            borderBottom : '2px black solid'
        }

        return (
            <div style={style}>
                <Post 
                    key="first_post"
                    data={firstPost}
                />

                <p>
                    Показано {lastPosts.length} последних постов. Нажмите здесь чтобы посмотреть весь тред
                </p>

                {lastPosts.map((el, id) => (
                    <Post 
                        key={id}
                        data={el}
                    />
                ))}
            </div>
        )
    }
    
    render() {
        const mode = this.props.mode || Thread.FULL_COLUMN;

        if (mode === Thread.COLUMN) {
            return this.columnThread();
        } else {
            return null;
        }
    }
}

export default Thread;