import React, { Component } from 'react';
import axios from 'axios';
import { connect } from 'react-redux';

import SearchWrapper from '../../../core/Search/Search.jsx';

import { BASE_REST_URL } from '../../../constants.js';

import { changeSearchResults } from '../../../store/actions/actions.js';

const Search = SearchWrapper('thread');

const mapDispatchToProps = dispatch => {
    return {
        changeThreads : threads => dispatch(changeSearchResults(threads))
    }
}

class ThreadSearch extends Component {
    handleRequest = url => {
        return axios.get(url);
    }

    handleResponse = response => {
        const threads = response.data;
        this.props.changeThreads(threads);
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

export default connect(null, mapDispatchToProps)(ThreadSearch);