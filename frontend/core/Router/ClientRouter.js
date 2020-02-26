import Router from "./Router.js";

/**
 * @typedef {import('./Route').Route} Route
 */

/**
 * @param  {...Route} routes
 * @returns {(context ?: Object) => any}
 */
const ClientRouter = (...routes) =>
  Router.apply(null, routes).bind(
    null,
    window.location.pathname,
    window.location.search
  );

export default ClientRouter;
