import React from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../config.js';

import Menu from '../../components/Menu/Menu.jsx';

const Board = ({ menu }) => (
    <>
        <div id="menu">
            <Menu 
                {...menu}
            />
        </div>
    </>
);

Board.getInitialProps = async ({ abbr }) => {
    try {
        const response = await axios.get(`${BASE_REST_URL}/main_get/`);
        return {
            menu : { boards : response.data, userboardService : {
                key : 'userboards',
                link : '/userboards/',
                title : 'Юзердоски'
            }, support : {
                key : 'support',
                link : '/support/',
                title : 'Поддержка'
            }, currentLink : `/boards/${abbr}`}
        };
    } catch (err) {
        console.log(err);
        return {};
    }
}

export default Board;