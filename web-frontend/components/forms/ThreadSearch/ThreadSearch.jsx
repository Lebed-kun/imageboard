import React, { Component } from 'react';
import { Form } from 'antd';
import axios from 'axios';

import SearchWrapper from '../../../core/Search/Search.jsx';

import { BASE_REST_URL } from '../../../constants.js';

const Search = SearchWrapper('thread');

class ThreadSearch extends Component {
    handleRequest = url => {
        return axios.get(url);
    }

    handleResponse = response => {
        console.log(response);
    }

    getUrl = () => {
        const board = this.props.board.abbr;
        return `${BASE_REST_URL}/main_get/boards/${board}/`;
    }
    
    render() {
        return (
            <Search 
                onRequest={this.handleRequest}
                onResponse={this.handleResponse}
                searchUrl={this.getUrl()}
            />
        )
    }
}

export default ThreadSearch;