import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { WebSocketServer } from 'ws';
import https from 'https';
import fs from 'fs';

// Create an instance of the Express application
const app = express();

// Resolve the current directory name (ESM doesn't have __dirname by default)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load SSL certificate and key
const options = {
    key: fs.readFileSync('server.key'),  // Path to your key file
    cert: fs.readFileSync('server.cert') // Path to your cert file
};

// Set the port for the server
const PORT = process.env.PORT || 3000;

// Serve static files (HTML, CSS, JS, assets) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Default route to serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the HTTPS server
const server = https.createServer(options, app).listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on https://<YOUR_LOCAL_IP>:${PORT}`);
});

// Create WebSocket server
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
    console.log('Client connected');
    ws.on('message', (message) => {
        console.log('received: %s', message);
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

// Send the position data over WebSocket
function sendPositionData(data) {
    wss.clients.forEach((client) => {
        if (client.readyState === client.OPEN) {
            client.send(JSON.stringify(data));
        }
    });
}

export { sendPositionData };
    
//https://192.168.1.182:3000
