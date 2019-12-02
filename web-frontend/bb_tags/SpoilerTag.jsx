import React from 'react';
import { Tag } from 'bbcode-to-react';

import styles from './SpoilerTag.css';

class SpoilerTag extends Tag {
    toReact() {
        return (
            <span className={styles.tag}>
                {this.getComponents()}
            </span>
        )
    }
}

export default SpoilerTag;