import http from 'http';

import router from './routes/server.js';

const server = http.createServer((req, res) => {
    try {
        const [path, query] = req.url.split('?');
        router.apply(null, [path, query, { req, res }]);
    } catch (err) {
        res.statusCode = 500;
        res.write(err.stack);
        res.end();
    }
});

server.listen(process.env.PORT || 8081, () => {
    console.log(`Server runs on port ${process.env.PORT || 8081}`);
});

export default server;