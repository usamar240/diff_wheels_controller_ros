# imports from library
from controller import Robot
import time

# imports from my code directory
from pose import Pose
from my_controller import Controller as Cont
from goal_controller import GoalController

# Variables
TIME_STEP = 64
sampling_period = 1

# Initializing Objects
robot = Robot()
pose_sense = robot.getDevice("gps")
rot = robot.getDevice("inertial")
target_goal = Pose()
goal_info = GoalController()
R5 = Cont()

# Goal position
target_goal.x = .4
target_goal.y = .5


# a function that makes pose similar to the one I have in ROS node
def make_pose(position, angle):
    r_pose = Pose()
    r_pose.x = position[0]
    r_pose.y = 1 - position[2]
    r_pose.theta = angle
    return r_pose


# Initial attributes and setup
pose_sense.enable(samplingPeriod=sampling_period)
rot.enable(samplingPeriod=sampling_period)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

time.sleep(1)

# Main loop
while robot.step(TIME_STEP) != -1:
    # Getting and Converting Sensor Data
    pos_val = pose_sense.getValues()
    rotation = rot.getRollPitchYaw()
    current_position = make_pose(pos_val, rotation[2])

    # Sending data to get final velocities
    desired_speeds = goal_info.get_velocity(current_position, target_goal, 3)
    lin = desired_speeds.xVel
    ang = desired_speeds.thetaVel
    speed = R5.getSpeeds(lin, ang)

    wheels[0].setVelocity(speed.left)
    wheels[1].setVelocity(speed.right)
    wheels[2].setVelocity(speed.left)
    wheels[3].setVelocity(speed.right)
