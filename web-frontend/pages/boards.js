import React from 'react';
import Head from 'next/head';
import axios from 'axios';
import { Layout, Pagination } from 'antd';
import Parser from '../bb_tags/register.js';
import tags from '../bb_tags/tags.js';
import 'antd/dist/antd.less';
import Router from 'next/router';
import withRedux from 'next-redux-wrapper';

import Menu from '../components/views/Menu/Menu.jsx';
import PostForm from '../components/forms/PostForm/PostForm.jsx';
import ThreadSearch from '../components/forms/ThreadSearch/ThreadSearch.jsx'; 
import ThreadList from '../components/views/ThreadList/ThreadList.jsx';

import makeStore from '../store/store.js';

import { BASE_REST_URL } from '../constants.js';
import { changeSearchResults } from '../store/actions/actions.js';

const { Header, Content } = Layout;

const THREADS_PER_PAGE = 10;

let BoardsPage = props => {
    Parser.registerTags(tags);

    const threadsCount = THREADS_PER_PAGE * props.threads.pages_count;

    const handlePageChange = page => {
        Router.push(`/boards/${props.board.abbr}?page=${page}`);
    }

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

                    <ThreadSearch board={props.board} />

                    <ThreadList
                        data={props.threads.results} 
                    />

                    <Pagination 
                        total={threadsCount}
                        pageSize={THREADS_PER_PAGE}
                        onChange={handlePageChange}
                    />
                </Content>
            </Layout>
        </>
    )
}

BoardsPage.THREADS_PER_PAGE = 10;

BoardsPage.getInitialProps = async ({ query : { abbr, page }, store }) => {
    let boards = await axios.get(`${BASE_REST_URL}/main_get/`);
    boards = boards.data;
    
    let threadsUrl = `${BASE_REST_URL}/main_get/boards/${abbr}/`;
    threadsUrl += page ? `?page=${page}` : '';
    let threads = await axios.get(threadsUrl);
    threads = threads.data;

    store.dispatch(changeSearchResults(threads));

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
        }
    }
}

BoardsPage = withRedux(makeStore, state => {
    return {
        threads : state.threads
    }
})(BoardsPage);

export default BoardsPage;