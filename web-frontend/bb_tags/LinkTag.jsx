import React from 'react';
import { Tag } from 'bbcode-to-react';

import styles from './LinkTag.less';

class LinkTag extends Tag {
    getProps() {
        return {
            className : styles.tag,
            href : this.params.to
        }
    }
    
    toReact() {
        return (
            <a {...this.getProps()}>
                {this.getComponents()}
            </a>
        )
    }
}

export default LinkTag;