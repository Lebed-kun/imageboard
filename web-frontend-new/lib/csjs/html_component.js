import { Component } from './component.js';

class HTMLComponent extends Component {
    constructor({ tag = '', attrs = {}, listeners = {}, children = {}, root = null, template = null }) {
        super({ props : {
            tag : tag,
            attrs : attrs,
            listeners : listeners,
            children : children
        }, root, template });
    }

    tree() {
        return {
            type : this._props.tag,
            attrs : this._props.attrs,
            listeners : this._props.listeners,
            children : this._props.children
        }
    }
}

export default HTMLComponent;