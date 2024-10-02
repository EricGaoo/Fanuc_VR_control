import asyncio
import websockets
import ssl
from robolink import *  # RoboDK API
from robodk import *    # RoboDK math functions

# Set up SSL context for secure WebSocket (WSS)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="server.cert", keyfile="server.key")  # Replace with your actual paths

# Connect to RoboDK and get the robot
RDK = Robolink()
robot = RDK.Item('YourRobotName', ITEM_TYPE_ROBOT)  # Replace 'YourRobotName' with your actual robot name

# Function to process incoming WebSocket connections and data
async def handle_data(websocket, path):
    print(f"New WebSocket connection established from {websocket.remote_address}")  # Connection confirmation
    try:
        async for message in websocket:
            # Parse the received data as [x, y, z]
            try:
                coordinates = [float(value) for value in message.strip("[]").split(",")]
                if len(coordinates) == 3:
                    x, y, z = coordinates
                    print(f"Received coordinates: {coordinates}")

                    # Define the target Cartesian position
                    target_position = [x, y, z]

                    # Set the target pose (orientation can be set to zero if not needed)
                    target_pose = Mat([[1, 0, 0, target_position[0]],
                                       [0, 1, 0, target_position[1]],
                                       [0, 0, 1, target_position[2]],
                                       [0, 0, 0, 1]])  # Homogeneous transformation matrix

                    # Solve inverse kinematics to get joint angles
                    joint_angles = robot.SolveIK(target_pose)

                    if joint_angles:
                        # Move the robot to the calculated joint angles
                        robot.MoveJ(joint_angles)
                        print(f"Moved robot to: {coordinates}")
                    else:
                        print("No solution found for the given Cartesian position.")
                else:
                    print("Invalid coordinate format received.")
            except Exception as e:
                print(f"Error processing coordinates: {e}")
    except websockets.ConnectionClosed:
        print("WebSocket connection closed")

# Start WebSocket server with SSL
start_server = websockets.serve(handle_data, "0.0.0.0", 8765, ssl=ssl_context)

# Start the event loop to handle WebSocket connections
print("WebSocket Secure (WSS) server is running on wss://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
