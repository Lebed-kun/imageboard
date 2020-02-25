import parser from 'bbcode-to-react';

const Parser = new parser.Parser();

const registerTags = function(tags) {
    tags.forEach(el => el.component && this.registerTag(
        el.tag,
        el.component
    ))
}

Parser.registerTags = registerTags;

export default Parser;