import React from 'react';
import { Card } from 'antd';

const About = props => {
    return (
        <Card>
            {props.info}
        </Card>
    )
}

export default About;