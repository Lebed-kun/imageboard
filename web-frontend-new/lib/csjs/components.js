class TextContent {
    constructor(text) {
        this._text = text;
    }

    _hydrateElement($text) {
        this.$element = $text;
    }

    _createElement() {
        const $element = document.createTextNode(this._text);
        this.$element = $element;
        return $element
    }

    _updateElement($parent, currTree, prevTree, index = 0) {
        const $children = $parent.childNodes;
        const $element = $children[index];
        
        if (prevTree === undefined || prevTree === null) {
            const $newElement = this._createElement();
            $parent.insertBefore($newElement, $element);
            return;
        }

        if (currTree === undefined || prevTree === null) {
            $parent.removeChild($element);
            return;
        }
        
        if (currTree !== prevTree) {
            const $newElement = this._createElement();
            $parent.replaceChild($newElement, $children[index]); 
        }
    }

    tree() {
        return this._text;
    }

    template() {
        return this._text;
    }
}

class Component {
    constructor({ props = {}, root = null, template = null }) {
        this._props = props;

        if (template) {
            this._hydrateElement(template);
        } else if (root) {
            this._createElement(root);
        }

        if (typeof window !== 'undefined' && this.unmounted) {
            window.addEventListener('beforeunload', this.unmounted.bind(this));
        }

        if (typeof window !== 'undefined' && this.mounted) {
            this.mounted();
        }
    }

    _hydrateElement($template) {
        const component = this.toComponent ? this.toComponent() : this;
        const tree = component.tree();

        this.$element = $template;

        this._setEventListeners($template, tree.listeners);

        const children = tree.children;
        if (!children) return;

        const $domChilds = $template.childNodes;
            
        for (let i = 0; i < children.length; i++) {
            if (!$domChilds[i]) {
                const $newElement = children[i]._createElement();
                $template.insertBefore($newElement, $domChilds[i]);
            } else {
                children[i]._hydrateElement($domChilds[i]);
            }
        }
    }

    _createElement($root = null) {
        const component = this.toComponent ? this.toComponent() : this;
        const tree = component.tree();
        const $element = document.createElement(tree.type);

        this._setAttributes($element, tree.attrs);
        this._setEventListeners($element, tree.listeners);

        const children = tree.children;
        for (let key in children) {
            const child = children[key];
            let $child = null;

            if (child instanceof Component || child instanceof TextContent) {    
                $child = child._createElement();
            }

            if ($child) {
                $element.appendChild($child);
            }
        }

        this.$element = $element;

        if ($root) {
            $root.appendChild($element);
        }
      
        return $element;
    }

    _setAttributes($element, attrs) {
        for (let key in attrs) {
            const value = attrs[key].toString();
            $element.setAttribute(key, value);
        }
    }

    _removeAttributes($element, attrs) {
        for (let key in attrs) {
            $element.removeAttribute(key);
        }
    }

    _setEventListeners($element, listeners) {
        for (let key in listeners) {
            const listener = listeners[key];
            $element[`on${key}`] = listener;
        }
    }


    _removeEventListeners($element, listeners) {
        for (let key in listeners) {
            $element[`on${key}`] = null;
        }
    }

    _updateElement($parent, currTree, prevTree, index = 0, prevIndex = null) {
        const $children = $parent.childNodes;
        const $element = typeof index === 'number' ? $children[index] : index;
        const $prevElement = prevIndex ? $children[prevIndex] : null;

        if (!prevTree) {
            const $newElement = this._createElement();
            $parent.insertBefore($newElement, $element);
            return;
        }

        if (!currTree) {
            $parent.removeChild($element);
            if (this.unmounted) this.unmounted();
            return;
        }
        
        if (currTree.type !== prevTree.type) {
            const $newElement = this._createElement();
            $parent.replaceChild($newElement, $element);
            return;
        } else {
            this._diffAttributes($prevElement || $element, currTree.attrs, prevTree.attrs);
            this._diffEventListeners($prevElement || $element, currTree.listeners, prevTree.listeners);
            this._diffChildren($prevElement || $element, currTree.children, prevTree.children);
        }

        if ($prevElement) {
            const $prevElementCopy = $prevElement.cloneNode(true);
            const $elementCopy = $element.cloneNode(true);

            $parent.replaceChild($prevElementCopy, $element);
            $parent.replaceChild($elementCopy, $prevElement);
        }
    }

    _diffChildren($parent, currChildren, prevChildren) {
        if (!currChildren && !prevChildren) {
            return;
        }

        const currKeys = Object.keys(currChildren);
        const prevKeys = Object.keys(prevChildren);

        for (let i = 0; i < currKeys.length; i++) {
            let currComponent = currChildren[currKeys[i]];
            currComponent = currComponent.toComponent ? currComponent.toComponent() : currComponent;

            const currTree = currComponent.tree();
            
            if (currKeys[i] !== prevKeys[i] && prevChildren[currKeys[i]]) {
                let prevComponent = prevChildren[currKeys[i]];
                prevComponent = prevComponent.toComponent ? prevComponent.toComponent() : prevComponent;

                const prevTree = prevComponent.tree();

                const j = prevKeys.findIndex(el => el === currKeys[i]);

                currComponent._updateElement($parent, currTree, prevTree, i, j);
            } else {
                let prevComponent = prevChildren[prevKeys[i]];
                if (prevComponent) {
                    prevComponent = prevComponent.toComponent ? prevComponent.toComponent() : prevComponent;
                }
                
                const prevTree = prevComponent ? prevComponent.tree() : null;
                currComponent._updateElement($parent, currTree, prevTree, i);
            }
        }

        const k = currKeys.length;
        for (let i = k; i < prevKeys.length; i++) {
            let prevComponent = prevChildren[prevKeys[i]];
            prevComponent = prevComponent.toComponent ? prevComponent.toComponent() : prevComponent;

            const prevTree = prevComponent.tree();

            prevComponent._updateElement($parent, null, prevTree, k);
        }
    }

    _diffAttributes($element, currAttrs, prevAttrs) {
        if (currAttrs && !prevAttrs) {
            this._setAttributes($element, currAttrs);
            return;
        }

        if (!currAttrs && prevAttrs) {
            this._removeAttributes($element, prevAttrs);
            return;
        }
        
        if (currAttrs && prevAttrs) {
            const currKeys = Object.keys(currAttrs);
            const prevKeys = Object.keys(prevAttrs);

            for (let i = 0; i < currKeys.length || i < prevKeys.length; i++) {
                const currAttr = currKeys[i];
                const prevAttr = prevKeys[i];

                if (prevAttr && currAttrs[prevAttr] === undefined) {
                    $element.removeAttribute(prevAttr);
                } 
                
                if (currAttr && currAttrs[currAttr] !== prevAttrs[currAttr]) {
                    const currValue = currAttrs[currAttr].toString();
                    $element.setAttribute(currAttr, currValue);
                } 
            }
        }
    }

    _diffEventListeners($element, currListeners, prevListeners) {
        if (currListeners && !prevListeners) {
            this._setEventListeners($element, currListeners);
            return;
        }

        if (!currListeners && prevListeners) {
            this._removeEventListeners($element, prevListeners);
            return;
        }

        if (currListeners && prevListeners) {
            const currKeys = Object.keys(currListeners);
            const prevKeys = Object.keys(prevListeners);

            for (let i = 0; i < currKeys.length || i < prevKeys.length; i++) {
                const currHandler = currKeys[i];
                const prevHandler = prevKeys[i];

                if (prevHandler && currListeners[prevHandler] === undefined) {
                    $element[`on${prevHandler}`] = null;
                } 
                
                if (currHandler && currListeners[currHandler] !== prevListeners[currHandler]) {
                    const listener = currListeners[currHandler];
                    $element[`on${currHandler}`] = listener;
                } 
            }
        }
    }

    _prepareAttributes(attrs) {
        let result = ''
        
        for (let key in attrs) {
            const value = attrs[key].toString();
            result += `${key}="${value}" `
        }

        return result;
    }

    setProps(props = {}) {
        const $element = this.$element;
        const $parent = $element.parentNode;

        let component = this.toComponent ? this.toComponent() : this;
        const prevTree = component.tree();

        const prevProps = this._props;
        this._props = Object.assign({}, this._props, props);

        component = this.toComponent ? this.toComponent() : this;
        const currTree = component.tree();

        this._updateElement($parent, currTree, prevTree, $element);

        if (this.updated) {
            this.updated(prevProps);
        }
    }

    getElement() {
        return this.$element;
    }
    
    tree() {
        return {
            type : '', // HTML tag name
            attrs : {}, // HTML attributes
            listeners : {}, // event listeners
            children : {} // another components and texts
        }
    }

    template() {
        const component = this.toComponent ? this.toComponent() : this;
        const tree = component.tree();

        let html = `<${tree.type} `;
        html += `${this._prepareAttributes(tree.attrs)}>`;

        const children = tree.children;
        for (let ch in children) {
            if (children[ch] instanceof Component || children[ch] instanceof TextContent) {
                html += children[ch].template();
            }
        }

        html += `</${tree.type}>`;

        return html;
    }
}

export { Component, TextContent };