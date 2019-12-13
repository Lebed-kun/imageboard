import parser from 'bbcode-to-react';

import UnderlineTag from './UnderlineTag.jsx';
import StrikeTag from './StrikeTag.jsx';
import SpoilerTag from './SpoilerTag.jsx';

const Parser = new parser.Parser();

const registerTags = function() {
    this.registerTag('u', UnderlineTag);
    this.registerTag('s', StrikeTag);
    this.registerTag('spoiler', SpoilerTag);
}

Parser.registerTags = registerTags;

export default Parser;