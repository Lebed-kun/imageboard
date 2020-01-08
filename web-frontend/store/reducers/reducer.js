import * as actionTypes from '../actions/types.js';

const changeSearchResults = (state, action) => {
    return Object.assign({}, state, {
        threads : action.threads
    })
}

const reducer = () => {
    const handlers = {
        [actionTypes.CHANGE_SEARCH_RESULTS] : changeSearchResults,
    }
    
    return (state, action) => {
        const handler = handlers[action.type];
        return handler ? handler(state, action) : state;
    }
}

export default reducer();