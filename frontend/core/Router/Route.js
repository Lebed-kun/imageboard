/**
 *
 * @typedef {Object} Route
 * @property {Array<string>} path
 * @property {(params : Object, query : Object) => any} handle
 * @property {boolean} exact
 */

/**
 *
 * @param {string} path
 * @param {(params : Object, query : Object) => any} handle
 * @param {?boolean} exact
 *
 * @returns {Route}
 */
const Route = (path, handle, exact = false) => ({
    path: path.split("/").filter(str => str),
    handle,
    exact
  });
  
  export default Route;
  