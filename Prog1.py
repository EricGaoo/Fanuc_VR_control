from robolink import *  # RoboDK API
from robodk import *  # RoboDK math functions

# Connect to RoboDK
RDK = Robolink()

# Get the robot you want to control
robot = RDK.Item('YourRobotName', ITEM_TYPE_ROBOT)

count = 0

while True:

    count+=1
    
    # Desired Cartesian position in mm
    target_position = [0,count,count]  # [x, y, z]

    # Set the target pose (orientation can be set to zero if not needed)
    target_pose = Mat([[1, 0, 0, target_position[0]],
                       [0, 1, 0, target_position[1]],
                       [0, 0, 1, target_position[2]],
                       [0, 0, 0, 1]])  # Homogeneous transformation matrix

    # Get the joint angles using inverse kinematics
    joint_angles = robot.SolveIK(target_pose)

    if joint_angles:
        # Move the robot to the calculated joint angles
        robot.MoveJ(joint_angles)
        print(count)
        print(joint_angles)
    else:
        print("No solution found for the given Cartesian position.")
