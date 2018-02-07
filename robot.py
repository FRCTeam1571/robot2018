
#!/usr/bin/env python3

import wpilib
from wpilib import drive
from wpilib import timer
import ctre
# from networktables import networktables


class robot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot Initiation'''

        self.controller = wpilib.XboxController(0)


        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.rr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.right = wpilib.SpeedControllerGroup(self.fr_motor, self.rr_motor)

        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.rl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.left = wpilib.SpeedControllerGroup(self.fl_motor, self.rl_motor)


        # self.rr_motor.set(mode(Follower))
        # self.rr_motor.set(self.fr_motor.getDeviceID())
        # self.rl_motor.set(mode(Follower))
        # self.rl_motor.set(self.fl_motor.getDeviceID())



        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        wpilib.timer.reset()
        wpilib.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        while self.isAutonomous() and self.isEnabled():
            # Drive for two seconds
            if self.timer.get() < 2.0:
                self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
            else:
                self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopInit(self):
        """This function is run once each time the robot enters telepo mode"""
        self.TriggerLeft = self.controller.getTriggerAxis()
        self.kLeft = self.controller.Hand.kLeft
        self.kRight = self.controller.Hand.kRight

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        # NOTE: For Deploy
        while self.isOperatorControl() and self.isEnabled():

            # backwards control
            if self.controller.getBumper(self.kLeft):
                self.TriggerLeft = self.TriggerLeft * -1

            # if self.controller.getTriggerAxis(self.kLeft) < 0:
            #     self.TriggerLeft = 0
            # elif self.controller.getTriggerAxis(self.kRight) > 0:
            #     self.TriggerLeft = 0

            if self.controller.getBumper(self.kRight):
                self.TriggerRight = self.TriggerRight * -1


            self.drive.arcadeDrive(self.TriggerLeft, self.controller.getX(self.kLeft))
        # NOTE: For Simulator
        # self.drive.tankDrive(self.controller.getRawAxis(1), self.controller.getRawAxis(3))


if __name__ == "__main__":
    wpilib.run(robot,
            physics_enabled=True)
