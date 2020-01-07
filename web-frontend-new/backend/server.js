import http from 'http';

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-type' : 'text/html' });
    
    console.log(req.url);
    
    res.write('Chi-chan');
    res.end();
})

server.listen(3000);