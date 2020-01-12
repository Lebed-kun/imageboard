import * as actionTypes from '../actions/types.js';

const changeSearchResults = (state, action) => {
    return Object.assign({}, state, {
        threads : action.threads
    })
}

const changePosts = (state, action) => {
    return Object.assign({}, state, {
        posts : action.posts
    })
}

const reducer = () => {
    const handlers = {
        [actionTypes.CHANGE_SEARCH_RESULTS] : changeSearchResults,
        [actionTypes.CHANGE_POSTS] : changePosts
    }
    
    return (state, action) => {
        const handler = handlers[action.type];
        return handler ? handler(state, action) : state;
    }
}

export default reducer();