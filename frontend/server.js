import http from 'http';

import router from './routes/server.js';

const server = http.createServer((req, res) => {
    const [path, query] = req.url.split('?');
    router.apply(null, [path, query, { req, res }]);
});

server.listen(process.env.PORT || 8080, () => {
    console.log(`Server runs on port ${process.env.PORT || 8080}`);
});

export default server;