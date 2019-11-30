import React from 'react';
import { Card } from 'antd';

const About = props => {
    return (
        <Card>
            <div dangerouslySetInnerHTML={{ __html : props.info }} />
        </Card>
    )
}

export default About;