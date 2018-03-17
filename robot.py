
#!/usr/bin/env python3
#Modified: 3/17

import wpilib
from wpilib import drive, Timer
import ctre
from networktables import NetworkTables




class robot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot Initiation'''

        NetworkTables.initialize(server='roborio-1571-frc.local')
        self.sd = NetworkTables.getTable('SmartDashboard')



        wpilib.CameraServer.launch('vision.py:main')





        self.controller0 = wpilib.XboxController(0)
        self.controller1 = wpilib.XboxController(1)

        # Talon SRX #
        # Right drivetrain
        self.fr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(2) #2
        self.rr_motor = ctre.wpi_talonsrx.WPI_TalonSRX(3) #3
        self.right = wpilib.SpeedControllerGroup(self.fr_motor, self.rr_motor)

        # Left drivetrain
        self.fl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(0) #0
        self.rl_motor = ctre.wpi_talonsrx.WPI_TalonSRX(1) #1
        self.left = wpilib.SpeedControllerGroup(self.fl_motor, self.rl_motor)

        # Middle motor ###UNUSED###
        self.mid_motor = ctre.wpi_talonsrx.WPI_TalonSRX(5)


        # Talon SR #
        # Grab motors
        self.intake_r = wpilib.Talon(0) #0
        self.intake_l = wpilib.Talon(1) #1
        self.intake = wpilib.SpeedControllerGroup(self.intake_r, self.intake_l)

        # Relay #
        # Loader
        self.loader = wpilib.Relay(1) #0

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
            if self.timer.get() > 0.0 and self.timer.get() < 10.0:
                self.drive.arcadeDrive(0.5, 0)  # Drive forwards at half speed
            else:
                self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopInit(self):
        """This function is run once each time the robot enters teleop mode"""
        self.kLeft = self.controller0.Hand.kLeft
        self.kRight = self.controller0.Hand.kRight
        self.lift.set(False)
        self.grab.set(False)
        self.GrabToggle = False
        self.GrabLast = False




    def teleopPeriodic(self):

        """This function is called periodically during operator control."""
        while self.isOperatorControl() and self.isEnabled():

            # Sets triggers and bumpers each loop
            self.TriggerLeft = self.controller0.getTriggerAxis(self.kLeft)
            self.TriggerRight = self.controller0.getTriggerAxis(self.kRight)
            self.BumperLeft = self.controller0.getBumper(self.kLeft)
            self.BumperRight = self.controller0.getBumper(self.kRight)


            # backwards control
            if self.BumperLeft:
                self.TriggerLeft = self.TriggerLeft * -1

            # if self.BumperRight:
            #     self.TriggerRight = self.TriggerRight * -1

            # Drive #
            self.drive.arcadeDrive(self.TriggerLeft, self.controller0.getX(self.kLeft))

            # Middle wheel #
            # trigger control
            # self.mid_motor.set(self.TriggerRight)
            # stick control
            # if abs(self.controller0.getX(self.kRight)) > 0.2:
            #     self.mid_motor.set(self.controller0.getX(self.kRight))
            # else:
            #     self.mid_motor.set(0.0)

            # Intake Motors #
            if self.controller0.getBButton():
                self.intake.set(0.25)
            elif self.controller0.getYButton():
                self.intake.set(-0.25)
            else:
                self.intake.set(0)

            # Solenoids #
            # Lift
            if self.controller0.getAButtonPressed() and not self.lift.get():
                self.lift.set(True)
            elif self.controller0.getAButtonReleased() and self.lift.get():
                self.lift.set(False)

            # Grabber
            if self.controller0.getXButton() and not self.GrabLast:
                 self.GrabToggle = not self.GrabToggle

            self.GrabLast = self.controller0.getXButton()
            self.grab.set(self.GrabToggle)

            # Loader #
            # Control
            if self.controller1.getAButton():
                self.loader.set(wpilib.Relay.Value.kForward)
            elif self.controller1.getBButton():
                self.loader.set(wpilib.Relay.Value.kReverse)
            else:
                self.loader.set(wpilib.Relay.Value.kOff)

            # SmartDashboard
            self.relayvalue = self.loader.get()
            if self.relayvalue == wpilib.Relay.Value.kForward:
                self.relaybool = True
            else:
                self.relaybool = False

            self.sd.putNumber('Relay Value', self.loader.get())
            self.sd.putBoolean('Relay Fwd', self.relaybool)









if __name__ == "__main__":
    wpilib.run(robot,
            physics_enabled=True)
