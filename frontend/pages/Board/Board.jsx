import React from 'react';
import axios from 'axios';
import { Pagination } from 'antd';

import { BASE_REST_URL } from '../../config.js';

import Menu from '../../components/Menu/Menu.jsx';
import ThreadList from '../../components/ThreadList/ThreadList.jsx';
import Form from '../../components/PostForm/PostForm.jsx';

const THREADS_PER_PAGE = 10;

const Board = ({ menu, board, currentPage }) => (
    <>
        <div id="menu">
            <Menu 
                {...menu}
            />
        </div>

        <div id="form">
            <Form boardAbbr={board.board.abbr} />
        </div>

        <ThreadList 
            data={board.results}
        />

        {board.pages_count > 1 ? (
            <div id="pagination">
                <Pagination 
                    total={board.pages_count * THREADS_PER_PAGE}
                    pageSize={THREADS_PER_PAGE}
                    current={currentPage}
                />
            </div>
        ) : null}
    </>
);

Board.getInitialProps = async ({ abbr, page = 1 }) => {
    try {
        const boardsResponse = await axios.get(`${BASE_REST_URL}/main_get/`);
        const threadsResponse = await axios.get(`${BASE_REST_URL}/main_get/boards/${abbr}/?page=${page}`);
        return {
            menu : { boards : boardsResponse.data, userboardService : {
                key : 'userboards',
                link : '/userboards/',
                title : 'Юзердоски'
            }, support : {
                key : 'support',
                link : '/support/',
                title : 'Поддержка'
            }, currentLink : `/boards/${abbr}`},
            board : threadsResponse.data,
            currentPage : page
        };
    } catch (err) {
        console.log(err);
        return {};
    }
}

export default Board;