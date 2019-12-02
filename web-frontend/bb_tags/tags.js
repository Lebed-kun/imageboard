import React from 'react';

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
        icon : <span style={{ textDecoration : 'underline' }}>U</span>
    },
    {
        tag : 's',
        icon : <span style={{ textDecoration : 'line-through' }}>S</span>
    },
    {
        tag : 'spolier',
        icon : <span style={{ background : 'grey', color : 'transparent' }}>XXXX</span>
    }
];

export default tags;