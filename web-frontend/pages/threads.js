import React from 'react';
import Head from 'next/head';
import axios from 'axios';
import { Layout, Pagination } from 'antd';
import Parser from '../bb_tags/register.js';
import 'antd/dist/antd.less';
import Router from 'next/router';
import withRedux from 'next-redux-wrapper';

import Menu from '../components/views/Menu/Menu.jsx';
import PostForm from '../components/forms/PostForm/PostForm.jsx';
import Thread from '../components/views/Thread/Thread.jsx';

import makeStore from '../store/store.js';
import { changePosts } from '../store/actions/actions.js';

import { BASE_REST_URL } from '../constants.js';

const { Header, Content } = Layout;

let ThreadsPage = props => {
    Parser.registerTags();

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
                    <PostForm key="up_form" thread={props.threadId} />

                    <Thread data={props.posts} />

                    <PostForm key="down_form" thread={props.threadId} />
                </Content>
            </Layout>
        </>
    )
}

ThreadsPage.getInitialProps = async ({ query : { id }, store }) => {
    let boards = await axios.get(`${BASE_REST_URL}/main_get/`);
    boards = boards.data;

    const postsUrl = `${BASE_REST_URL}/main_get/threads/${id}/`;
    let posts = await axios.get(postsUrl);
    posts = posts.data;

    store.dispatch(changePosts(posts));

    return {
        title : `${posts[0].title}`,
        threadId : id,

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

ThreadsPage = withRedux(makeStore, state => {
    return {
        posts : state.posts
    }
})(ThreadsPage);

export default ThreadsPage;