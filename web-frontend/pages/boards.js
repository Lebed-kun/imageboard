import React from 'react';
import Head from 'next/head';
import axios from 'axios';
import { Layout } from 'antd';

import Menu from '../components/views/Menu/Menu.jsx';

import PostForm from '../components/forms/PostForm/PostForm.jsx'; 

import { BASE_REST_URL } from '../constants.js';

import 'antd/dist/antd.less';

const { Header, Content } = Layout;

const BoardsPage = props => {
    // TO DO : search form and threads
    
    return (
        <>
            <Head>
                <title>{props.title}</title>
            </Head>

            <Layout>
                <Header style={{ position : 'fixed', zIndex : 1, width : '100%' }}>
                    <Menu mode="horizontal" links={props.menuLinks}/>
                </Header>

                <Content style={{ paddingTop : '72px' }}>
                    <h1>{props.board.name}</h1>

                    <PostForm board={props.board.abbr} />
                </Content>
            </Layout>
        </>
    )
}

BoardsPage.getInitialProps = async ({ query : { abbr }}) => {
    let boards = await axios.get(`${BASE_REST_URL}/main_get/`);
    boards = boards.data;
    
    let threads = await axios.get(`${BASE_REST_URL}/main_get/boards/${abbr}/`);
    threads = threads.data;

    const currBoard = threads.board;

    return {
        board : currBoard,
        title : `/${currBoard.abbr}/ ${currBoard.name}`,

        menuLinks : {
            prev : [
                {
                    href : '/',
                    title : 'Главная'
                }
            ],
            boards : boards.map(el => {
                return {
                    href : `/boards/${el.abbr}`,
                    title : `/${el.abbr}/ ${el.name}`
                }
            }),
            next : [
                {
                    href : '/userboards',
                    title : 'Юзердоски'
                },
                {
                    href : '/suggest',
                    title : 'Техподдержка'
                }
            ]
        },

        threads
    }
}

export default BoardsPage;