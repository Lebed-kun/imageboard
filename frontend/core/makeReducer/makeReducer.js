/**
 *
 * @param {Object<string|number|symbol, (S, A) => S>} reducers
 * @returns {(S, A) => S}
 */
const makeReducer = reducers => (state, action) => {
    const reducer = reducers[action.type];
    return reducer ? reducer(state, action) : state;
  };
  
export default makeReducer;
  