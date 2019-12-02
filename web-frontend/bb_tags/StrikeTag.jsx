import React from 'react';
import { Tag } from 'bbcode-to-react';

class StrikeTag extends Tag {
    getStyle = () => {
        return {
            textDecoration : 'line-through'
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

export default StrikeTag;