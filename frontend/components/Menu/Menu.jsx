import React from 'react';
import { Layout, Menu } from 'antd';

const { Header } = Layout;
const { SubMenu } = Menu;

/**
 * @typedef {Object} Board
 * @property {string} name
 * @property {string} abbr
 * 
 * @param {Object} param0
 * @property {Array<Board>} boards
 * @property {Object} userboardService
 * @property {Object} support
 * 
 * @returns {React.ReactElement}  
 */
const CustomMenu = ({ boards, userboardService, support, currentLink, ...props }) => (
            <Header {...props}>
                <Menu mode="horizontal">
                    <SubMenu title="Доски">
                        {boards.map((el, id) => (
                            <Menu.Item key={id}>
                                <a href={`/boards/${el.abbr}`}>
                                    /{el.abbr}/ - {el.name}
                                </a>
                            </Menu.Item>
                        ))}
                    </SubMenu>

                    <Menu.Item key={userboardService.key}>
                        <a href={userboardService.link}>
                            {userboardService.title}
                        </a>
                    </Menu.Item>

                    <Menu.Item key={support.key}>
                        <a href={support.link}>
                            {support.title}
                        </a>
                    </Menu.Item>
                </Menu>
            </Header>
)

export default CustomMenu;