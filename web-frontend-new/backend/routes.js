import Router from '../lib/csjs/router.js';

const router = new Router();

router.handleRoute({
    exact : true,
    pattern : '/',
    handle : params => {
        const router = params.router;
        router.execute({
            params : params,
            url : '/boards/g/'
        })
    }
});

router.handleRoute({
    exact : true,
    pattern : '/boards/:abbr',
    handle : params => {
        // Render EJS template
    }
})