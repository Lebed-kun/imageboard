import React from 'react';
import { Tag } from 'bbcode-to-react';

class UnderlineTag extends Tag {
    getStyle = () => {
        return {
            textDecoration : 'underline'
        }
    }

    toReact() {
        return (
            <span style={this.getStyle()}>
                {this.getComponents()}
            </span>
        )
    }
}

export default UnderlineTag;