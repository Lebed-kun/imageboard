import React, { Component } from 'react';

const Preview = props => {
    let name = props.name.split('.');
    name = name[0].slice(0, 8) + '.' + name[1];

    const blockStyle = {
        display : 'inline-block',
        width : '200px',
    }

    const imageStyle = {
        width: '100%',
        height: 'auto'
    }

    return (
        <a href={props.url} style={blockStyle}>
            <img src={props.url} style={imageStyle}/>

            <p>
                {name}
            </p>
        </a>
    )
}

export default Preview;