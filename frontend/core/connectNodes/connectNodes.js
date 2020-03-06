/**
 *
 * @param {object} param0
 * @property {string|number|symbol} idProp
 * @property {string|number|symbol} textProp
 * @property {string|number|symbol} linkProp
 * @param {RegExp} linkPattern
 * @returns {Array<object> => void}
 */
export const connectNodes = ({ idProp, textProp, linkProp }, linkPattern) => {
    const resolveLinks = node => {
      const links = node[textProp].match(linkPattern);
      return links
        ? links.reduce(
            (list, link) => ({
              ...list,
              [link]: true
            }),
            {}
          )
        : null;
    };
  
    const attachLink = (node, currNum) => {
      if (!node[linkProp]) node[linkProp] = [];
      node[linkProp].push(currNum);
    };
  
    const attachLinks = (currLinks, currNode, nodes, ptr) => {
      for (let i = ptr - 1; i >= 0; i--) {
        const nodeId = nodes[i][idProp];
        if (currLinks[nodeId]) attachLink(nodes[i], currNode[idProp]);
      }
    };
  
    return nodes => {
      nodes.forEach((node, ptr) => {
        const links = resolveLinks(node);
        if (links) {
          attachLinks(links, node, nodes, ptr);
        }
      });
    };
  };