import React from 'react';
import { Tag } from 'bbcode-to-react';

import styles from './QuoteTag.less';

class QuoteTag extends Tag {
    toReact() {
        return (
            <blockquote className={styles.tag}>
                {this.getComponents()}
            </blockquote>
        )
    }
}

export default QuoteTag;