import React from 'react';
import axios from 'axios';

import { BASE_REST_URL } from '../../config.js';

import Menu from '../../components/Menu/Menu.jsx';

const Board = ({ boards, userboardService, support }) => (
    <>
        <div id="menu">
            <Menu 
                boards={boards}
                userboardService={userboardService}
                support={support}
            />
        </div>
    </>
);

Board.getInitialProps = async ({ abbr }) => {
    try {
        const response = await axios.get(`${BASE_REST_URL}/main_get/`);
        return { boards : response.data, userboardService : {
            key : 'userboards',
            link : '/userboards/',
            title : 'Юзердоски'
        }, support : {
            key : 'support',
            link : '/support/',
            title : 'Поддержка'
        }};
    } catch (err) {
        console.log(err);
        return {};
    }
}

export default Board;