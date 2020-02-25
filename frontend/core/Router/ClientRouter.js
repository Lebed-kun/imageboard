import Router from "./Router";

/**
 * @typedef {import('./Route').Route} Route
 */

/**
 * @param  {...Route} routes
 * @returns {() => any}
 */
const ClientRouter = (...routes) =>
  Router.apply(null, routes).bind(
    null,
    window.location.pathname,
    window.location.search
  );

export default ClientRouter;
