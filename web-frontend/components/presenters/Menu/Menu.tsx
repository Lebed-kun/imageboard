import React from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../../constants';

type MenuProps = {
    direction : string,
    extraLinks : Object[]
}

type MenuState = {
    links : Object[]
}

class Menu extends React.Component<MenuProps> {
    constructor(props) {
        super(props);
        
        let links = [];
        if (props.extraLinks) {
            links = props.extraLinks.map(el => {
                return {
                    href : el.href,
                    title : el.title
                }
            })
        }
        // To DO
    }

    getLinkTitle = (name : string, abbr : string) : string => {
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
        return { 
            links : this.state.links.concat(boardLinks)
        }
    }

    homeLink = () => {
        if (this.props.homeLink) {
            return (
                <a>

                </a>
            )
        }
    }
    
    render() {
        
        return (
            <div>

            </div>
        )
    }
}