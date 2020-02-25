import React from 'react';
import Head from 'next/head';
import axios from 'axios';
import { Layout, Pagination } from 'antd';
import 'antd/dist/antd.less';
import Router from 'next/router';
import withRedux from 'next-redux-wrapper';

import makeStore from '../store/store.js';

import { BASE_REST_URL } from '../constants.js';
import { changeSearchResults } from '../store/actions/actions.js';

const { Header, Content } = Layout;
const BOARDS_PER_PAGE = 10;

let UserBoardsPage = props => {
    return (
        <>
            <Head>
                Пользовательские доски
            </Head>

            <Content>
                {null}
            </Content>
        </>
    )
}

export default UserBoardsPage;
