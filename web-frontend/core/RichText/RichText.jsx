import React, { Component } from 'react';
import { Input, Button, Layout } from 'antd';

const { TextArea } = Input;
const { Header } = Layout;

class RichText extends Component {
    addTag = e => {
        const tag = e.currentTarget.getAttribute('tag');
        const setValue = this.props.setValue;
        
        setValue(`[${tag}][/${tag}]`);
    }
    
    renderBar = () => {
        const tags = this.props.tags;
        
        return (
            <Header>
                {tags.map((el, id) => (
                    <Button key={id} tag={el.tag} onClick={this.addTag}>
                        <div dangerouslySetInnerHTML={{__html : el.icon}} />
                    </Button>
                ))}
            </Header>
        )
    }
    
    render() {
        const fieldDecorator = this.props.fieldDecorator;

        return (
            <div>
                {this.renderBar()}

                {fieldDecorator(<TextArea />)}
            </div>
        )
    }
}

export default RichText;