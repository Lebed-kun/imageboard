import parser from 'bbcode-to-react';

import UnderlineTag from './UnderlineTag.jsx';
import StrikeTag from './StrikeTag.jsx';
import SpoilerTag from './SpoilerTag.jsx';

const registerTags = () => {
    parser.registerTag('u', UnderlineTag);
    parser.registerTag('s', StrikeTag);
    parser.registerTag('spoiler', SpoilerTag);
}

export default registerTags;