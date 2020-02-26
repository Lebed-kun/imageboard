import { isEmpty } from "../isEmpty/isEmpty.js";

/**
 * @typedef {import('./Route').Route} Route
 */

/**
 * @param  {...Route} routes
 * @returns {(path : string, query ?: string, context ?: Object) => any}
 */
const Router = (...routes) => (path, query, context) => {
  path = path.split("/").filter(str => str);
  query = !isEmpty(query)
    ? query
        .split(/[?&]/)
        .filter(str => str)
        .reduce((res, pair) => {
          const [key, value] = pair.split("=");
          return {
            ...res,
            [key]: !isEmpty(value) ? value : true
          };
        }, {})
    : {};

  const results = [];

  for (let i = 0; i < routes.length; i++) {
    let params = {};

    routes[i].path.forEach((str, id) => {
      if (params && str.match(/^\:/)) {
        params[str.slice(1)] = path[id];
      } else if (str !== "*" && str !== path[id]) {
        params = null;
      }
    });

    if (params && routes[i].exact) {
      return routes[i].handle(params, query, context);
    } else if (params) {
      const res = routes[i].handle(params, query, context);
      if (!isEmpty(res)) {
        results.push(res);
      }
    }
  }

  return results;
};

export default Router;
