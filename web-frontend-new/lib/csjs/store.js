class Store {
    constructor(initState = {}) {
      this._state = initState;
      this._listeners = {};
    }
  
    connect(Component) {
      const store = this;
  
      return class StoreComponent extends Component {
        constructor({ props = {}, root = null, template = null }) {
          super({
            props: Object.assign({}, props, {
              store: store
            }),
            root,
            template
          });
        }
  
        setProps(props = {}, state = null) {
          const $element = this.$element;
          const $parent = $element.parentNode;
  
          let component = this.toComponent ? this.toComponent() : this;
          const prevTree = component.tree();
  
          const prevState = store.getState();
          if (state) {
            store.setState(state);
          }
  
          const prevProps = this._props;
          if (props) {
            this._props = Object.assign({}, this._props, props);
          }
  
          component = this.toComponent ? this.toComponent() : this;
          const currTree = component.tree();
  
          this._updateElement($parent, currTree, prevTree, $element);
  
          if (this.updated) {
            this.updated(prevProps, prevState);
          }
        }
      };
    }
  
    subscribe(event, key, callback) {
      const listeners = this._listeners;
  
      if (!listeners[event]) {
        listeners[event] = {};
      }
  
      listeners[event][key] = callback;
    }
  
    unsubscribe(event, key) {
      const listeners = this._listeners;
      delete listeners[event][key];
    }
  
    dispatch(event, payload) {
      const listeners = this._listeners[event];
  
      for (let lis in listeners) {
        const callback = listeners[lis];
        callback(this._state, payload);
      }
    }
  
    getState() {
      return this._state;
    }
  
    setState(state) {
      this._state = state;
    }
  }
  
  export default Store;
  