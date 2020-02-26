import Router from "./Router";

/**
 * @typedef {import('./Route').Route} Route
 */

/**
 * @param  {...Route} routes
 * @returns {(context ?: Object) => any}
 */
const ClientRouter = (...routes) => context =>
  Router(...routes)(window.location.pathname, window.location.search, context);

export default ClientRouter;
