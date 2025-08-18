const http = require('http');

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });

    if (req.url === '/api/test') {
        res.end(JSON.stringify({
            status: 'ok',
            message: 'Simple server working!',
            timestamp: new Date().toISOString()
        }));
    } else {
        res.end(JSON.stringify({
            message: 'PaulyOps simple server is running ✅',
            endpoints: ['/api/test']
        }));
    }
});

const PORT = 8787;
server.listen(PORT, () => {
    console.log(`🚀 Simple server running on http://localhost:${PORT}`);
    console.log(`📡 Test: curl http://localhost:${PORT}/api/test`);
});
