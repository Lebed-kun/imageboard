import * as actionTypes from './types.js';

export const changeSearchResults = threads => {
    return {
        type : actionTypes.CHANGE_SEARCH_RESULTS,
        threads
    }
}