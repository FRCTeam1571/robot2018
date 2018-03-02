
#!/usr/bin/env python3
#Modified: 2/17

import wpilib
from wpilib import drive, Timer
import ctre
from networktables import NetworkTables

#import cscore

#import cv2
import numpy as np



class robot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot Initiation'''

        # NetworkTables.initialize(server='roborio-1571-frc.local')



        self.controller = wpilib.XboxController(0)

        # Talon SRX #
        # Right drivetrain
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(2) #2
        self.rr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(3) #3
        self.right = wpilib.SpeedControllerGroup(self.fr_motor, self.rr_motor)

        # Left drivetrain
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(0) #0
        self.rl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(1) #1
        self.left = wpilib.SpeedControllerGroup(self.fl_motor, self.rl_motor)

        # Middle motor
        self.mid_motor = ctre.wpi_talonsrx.WPI_TalonSRX(5)


        # Talon SR #
        # Grab motors
        self.intake_r = wpilib.Talon(0)
        self.intake_l = wpilib.Talon(1)
        self.intake = wpilib.SpeedControllerGroup(self.intake_r, self.intake_l)

        # Solenoids #
        self.lift = wpilib.Solenoid(0, 0)
        self.grab = wpilib.Solenoid(0, 1)

        self.timer = wpilib.Timer()

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        while self.isAutonomous() and self.isEnabled():
            # Drive for two seconds
            if self.timer.get() < 0.0:
                self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
            elif self.timer.get() < 5.0:
                self.drive.arcadeDrive(0, 0)
            else:
                self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopInit(self):
        """This function is run once each time the robot enters telepo mode"""
        self.kLeft = self.controller.Hand.kLeft
        self.kRight = self.controller.Hand.kRight
        self.lift.set(False)
        self.grab.set(False)
        self.GrabToggle = False
        self.GrabLast = False




    def teleopPeriodic(self):

        """This function is called periodically during operator control."""
        while self.isOperatorControl() and self.isEnabled():

            # Sets triggers and bumpers each loop
            self.TriggerLeft = self.controller.getTriggerAxis(self.kLeft)
            self.TriggerRight = self.controller.getTriggerAxis(self.kRight)
            self.BumperLeft = self.controller.getBumper(self.kLeft)
            self.BumperRight = self.controller.getBumper(self.kRight)


            # backwards control
            if self.BumperLeft:
                self.TriggerLeft = self.TriggerLeft * -1


            if self.BumperRight:
                self.TriggerRight = self.TriggerRight * -1

            # Drive #
            self.drive.arcadeDrive(self.TriggerLeft, self.controller.getX(self.kLeft))

            # Middle wheel
            # self.mid_motor.set(self.TriggerRight)
            self.mid_motor.set(self.controller.getX(self.kRight))

            if self.controller.getBButton():
                self.intake.set(0.25)
            elif self.controller.getYButton():
                self.intake.set(-0.25)
            else:
                self.intake.set(0)




            # Solenoids #

            if self.controller.getAButtonPressed() and self.lift.get() == False:
                self.lift.set(True)
            elif self.controller.getAButtonReleased() and self.lift.get() == True:
                self.lift.set(False)

            if self.controller.getXButton() and not self.GrabLast:
                self.GrabToggle = not self.GrabToggle

            self.GrabLast = self.controller.getXButton()


            if self.GrabToggle and self.GrabLast:
                self.grab.set(True)
            elif self.GrabLast:
                self.grab.set(False)








if __name__ == "__main__":
    wpilib.run(robot,
            physics_enabled=True)
