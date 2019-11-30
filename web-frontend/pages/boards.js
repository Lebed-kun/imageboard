import React from 'react';
import Head from 'next/head';
import axios from 'axios';

import Menu from '../components/views/Menu/Menu.jsx';

import { BASE_REST_URL } from '../constants.js';

import 'antd/dist/antd.less';

const BoardsPage = props => {
    <>
        <Head>
            <title>{props.title}</title>
        </Head>
    </>
}