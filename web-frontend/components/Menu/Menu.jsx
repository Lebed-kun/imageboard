import React, { Component } from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../constants.js';

class LinkMenu extends Component {
    state = {
        homeLink : '/',
        boardLinks : null
    }
    
    getInitialProps() {
        
    }
    
    render() {
        const Element = this.props.component;

        return (
            <Element>

            </Element>
        )
    }
}