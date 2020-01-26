import React from 'react';

import UnderlineTag from './UnderlineTag.jsx';
import StrikeTag from './StrikeTag.jsx';
import SpoilerTag from './SpoilerTag.jsx';
import LinkTag from './LinkTag.jsx';
import QuoteTag from './QuoteTag.jsx';

const tags = [
    {
        tag : 'b',
        icon : <b>B</b>
    },
    {
        tag : 'i',
        icon : <i>I</i>
    },
    {
        tag : 'u',
        icon : <span style={{ textDecoration : 'underline' }}>U</span>,
        component : UnderlineTag
    },
    {
        tag : 's',
        icon : <span style={{ textDecoration : 'line-through' }}>S</span>,
        component : StrikeTag
    },
    {
        tag : 'spoiler',
        icon : <span style={{ background : 'grey', color : 'transparent' }}>XXXX</span>,
        component : SpoilerTag
    },
    {
        tag : 'link',
        icon : <span style={{ textDecoration : 'underline', color : 'orange' }}>Link</span>,
        component : LinkTag
    },
    {
        tag : 'quote',
        icon : <span style={{ color : 'green' }}>« »</span>,
        component : QuoteTag
    }
];

export default tags;