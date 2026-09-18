const http = require('http');

const port = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
  if (req.url === '/healthz') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('OK');
  } else {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello, World!\n');
  }
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
