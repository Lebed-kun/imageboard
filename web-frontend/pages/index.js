import React from 'react';
import Head from 'next/head';
import { Row } from 'antd';
import axios from 'axios';

import LoginForm from '../components/forms/LoginForm/LoginForm.jsx';
import Menu from '../components/views/Menu/Menu.jsx';
import About from '../components/views/About/About.jsx';

import { BASE_REST_URL, BASE_URL } from '../constants.js';

const IndexPage = props => {
    return (
        <>
            <Head>
                <title>Chi-chan</title>
            </Head>

            <Row key="side">
                <LoginForm />

                <Menu links={props.links} />
            </Row>

            <Row key="info">
                <About info={props.info} />
            </Row>
        </>
    )
}

IndexPage.getInitialProps = async () => {
    const boards = await axios.get(`${BASE_REST_URL}/main_get/`);
    const info = await axios.get(`${BASE_REST_URL}/main_get/about/`);

    return {
        links : {
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

        info : info.info
    }
}

export default IndexPage;