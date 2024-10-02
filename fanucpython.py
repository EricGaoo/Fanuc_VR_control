import asyncio
import websockets
import ssl


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="server.cert", keyfile="server.key")  # Replace with your actual paths

# This function handles the incoming WebSocket connections
async def handle_data(websocket, path):
    print(f"New WebSocket connection established from {websocket.remote_address}")  # Connection confirmation
    try:
        async for message in websocket:
            print(f"Received data: {message}")
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

# Start WebSocket server with SSL
start_server = websockets.serve(handle_data, "0.0.0.0", 8765, ssl=ssl_context)

# Print server start confirmation
print("WebSocket Secure (WSS) server is running on wss://0.0.0.0:8765")

# Start event loop to handle connections
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
