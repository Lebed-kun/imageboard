import React from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../../constants';


class Menu extends React.Component {
    getLinkTitle = (name, abbr) => {
        if (this.props.direction === 'column' && abbr) {
            return `/${abbr}/ - ${name}`;
        } else {
            return name;
        }
    }
    
    static async getInitialProps() {
        const response = await axios.get(`${BASE_REST_URL}/main_get/`);
        const json = await response.json();
        const boardLinks = json.map(el => {
            return {
                href : `/boards/${el.abbr}`,
                title : this.getLinkTitle(el.name, el.abbr)
            }
        });
        return { boardLinks }
    }

    listLinks = links => {
        const column = this.props.direction === 'column';
        
        let list = null;
        if (links) {
            list = (
                <ul>
                    {column ? null : '[ '}
                    {links.map((el, id) => (
                        <li key={id}>
                            <a href={el.href}>
                                {el.title}
                            </a>
                            {column ? null : ' / '}
                        </li>
                    ))}
                    {column ? <hr /> : ' ] | '}
                </ul>
            )
        }

        return list;
    } 
    
    render() {
        const beforeLinks = this.listLinks(this.props.beforeLinks);
        const boardLinks = this.listLinks(this.props.boardLinks);
        const afterLinks = this.listLinks(this.props.afterLinks);

        return (
            <ul>
                <li key="before-links">
                    {beforeLinks}
                </li>

                <li key="board-links">
                    {boardLinks}
                </li>

                <li key="after-links">
                    {afterLinks}
                </li>
            </ul>
        )
    }
}