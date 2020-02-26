import React from 'react';
import { Layout, Menu, Select } from 'antd';
import { isClient } from '../../core/isClient/isClient.js';

const { Header } = Layout;
const { Option } = Select;

/**
 * @param {string} value 
 */
const handleSelectBoard = value => window.location.pathname = value;

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
const CustomMenu = ({ boards, userboardService, support, currentLink }) => (
            <Header>
                <Select onChange={isClient() ? handleSelectBoard : null} defaultValue={currentLink}>
                        {boards.map((el, id) => (
                            <Option key={id} value={`/boards/${el.abbr}`}>
                                /{el.abbr}/ - {el.name}
                            </Option>
                        ))}

                        <Option key={userboardService.key} value={userboardService.link}>
                            {userboardService.title}
                        </Option>

                        <Option key={support.key} value={support.link}>
                            {support.title}
                        </Option>
                    </Select>
            </Header>
)

export default CustomMenu;