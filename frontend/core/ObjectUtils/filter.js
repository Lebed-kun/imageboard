/**
 *
 * @param {object} obj
 * @param {(any, number|string|symbol, object) => boolean} func
 * @returns {object}
 */
const filter = (obj, func) => {
    const newObj = {};
    for (let key in obj) {
      if (func(obj[key], key, obj)) newObj[key] = obj[key];
    }
    return newObj;
  };
  
export default filter;
  