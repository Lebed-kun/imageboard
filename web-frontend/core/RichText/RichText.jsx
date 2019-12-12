import React, { Component } from 'react';
import { Input, Button, Layout } from 'antd';

const { TextArea } = Input;
const { Header } = Layout;

class RichText extends Component {
    state = {
        value : ''
    }
    
    addTag = e => {
        const tag = e.currentTarget.getAttribute('tag');
        const setValue = this.props.setValue;
        
        setValue(`[${tag}][/${tag}]`);
    }
    
    renderBar = () => {
        const tags = this.props.tags;

        if (!tags) {
            return null;
        }
        
        return (
            <Header>
                {tags.map((el, id) => (
                    <Button key={id} tag={el.tag} onClick={this.addTag}>
                        {el.icon}
                    </Button>
                ))}
            </Header>
        )
    }

    handleChange = e => {
        this.setState({
            value : e.currentTarget.value
        })
    }

    renderCounter = () => {
        const maxCount = this.props.maxCount;
        const currCount = this.state.value.length;

        return maxCount ? <p>{currCount} / {maxCount}</p> : null;
    }
    
    render() {
        const fieldDecorator = this.props.fieldDecorator || (component => component);

        return (
            <div>
                {this.renderBar()}

                {fieldDecorator(
                    <TextArea 
                        style={{ height : '12rem' }}
                        onChange={this.handleChange} 
                    />
                )}

                {this.renderCounter()}
            </div>
        )
    }
}

export default RichText;