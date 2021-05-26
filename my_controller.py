from __future__ import division

#import rospy


class MotorCommand:
    """Holds motor control commands for a differential-drive robot.
    """

    def __init__(self):
        self.left = 0
        self.right = 0


class Controller:
    """Determines motor speeds to accomplish a desired motion.
    """

    def __init__(self):
        # Set the max motor speed to a very large value so that it
        # is, essentially, unbound.
        self.maxMotorSpeed = 5  # ticks/s
        self.ticksPerMeter = 100
        self.wheelSeparation = .05

    def getSpeeds(self, linearSpeed, angularSpeed):
        tickRate = linearSpeed * self.ticksPerMeter
        diffTicks = angularSpeed * self.wheelSeparation * self.ticksPerMeter

        speeds = MotorCommand()
        speeds.left = tickRate - diffTicks
        speeds.right = tickRate + diffTicks

        # Adjust speeds if they exceed the maximum.
        if max(abs(speeds.left), abs(speeds.right)) > self.maxMotorSpeed:
            factor = self.maxMotorSpeed / max(abs(speeds.left), abs(speeds.right))
            speeds.left *= factor
            speeds.right *= factor

        return speeds

    def setWheelSeparation(self, separation):
        self.wheelSeparation = separation

    def setMaxMotorSpeed(self, limit):
        self.maxMotorSpeed = limit

    def setTicksPerMeter(self, ticks):
        self.ticksPerMeter = ticks
