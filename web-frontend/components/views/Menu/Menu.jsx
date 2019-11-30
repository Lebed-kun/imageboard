import React, { Component } from 'react';
import { Menu } from 'antd';

const SubMenu = Menu.SubMenu;
const Item = Menu.Item;

class LinkMenu extends Component {
    static HORIZONTAL = 'horizontal';
    static INLINE = 'inline';

    renderLinks = (type, title, condition = props => true) => {
        const links = this.props.links[type];
        if (links && condition(this.props)) {
            return (
                <SubMenu key={type} title={title}>
                    {links.map((el, id) => (
                        <Item key={id}>
                            <a href={el.href}>{el.title}</a>
                        </Item>
                    ))}
                </SubMenu>
            )
        } else {
            return null;
        }
        
    }

    renderMenu = () => {
        const boardLinks = this.props.links.boards;
        if (boardLinks) {
            return (
                <Menu mode={this.props.mode || LinkMenu.INLINE}>
                    {this.renderLinks('prev', 'Главная', props => props.mode === LinkMenu.HORIZONTAL)}
                    {this.renderLinks('boards', 'Доски')}
                    {this.renderLinks('next', 'Прочее')}
                </Menu>
            )
        } else {
            return null;
        }
    }
    
    render() {
        return this.renderMenu();
    }
}

export default LinkMenu;