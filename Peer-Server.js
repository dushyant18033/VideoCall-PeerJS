const fs = require('fs');
const { PeerServer } = require('peer');

const peerServer = PeerServer({
  port: 9000,
  ssl: {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem')
  }
});