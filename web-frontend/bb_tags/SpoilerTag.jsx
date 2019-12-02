import React from 'react';
import { Tag } from 'bbcode-to-react';

import styles from './SpoilerTag.less';

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