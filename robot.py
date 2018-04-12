
#!/usr/bin/env python3
#Modified: 3/30

# For Solenoids:
# False = Up
# True = Down

import wpilib
from wpilib import drive, Timer, SendableChooser
import ctre
from networktables import NetworkTables
import rangefinder



class robot(wpilib.IterativeRobot):

    def robotInit(self):
        '''Robot Initiation'''

        NetworkTables.initialize(server='roborio-1571-frc.local')
        self.table = NetworkTables.getTable('SmartDashboard')



        wpilib.CameraServer.launch('vision.py:main')





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

        # Ultrasonic Sensor #
        rangefinder.Maxbotultrasonic.Maxbotultrasonic(self, 0)
        self.ultrasonic = rangefinder.Maxbotultrasonic

        # self.chooser = wpilib.SendableChooser()
        # self.chooser.addDefault("Left", -1)
        # self.chooser.addObject("Right", 1)
        # wpilib.SmartDashboard.putData("Choice", self.chooser)
        # self.select = -1


    def disabledInit(self):
        # self.timer.reset()
        # self.timer.start()

        self.lift.set(False)

    def disabledPeriodic(self):

        # Ultrasonic test #
        # if self.timer.get() >= 2.0:
        #     self.timer.reset()
        #     self.timer.start()
        #     self.table.putNumber('Range In Inches', self.ultrasonic.GetRangeInInches(self))

        self.lift.set(False)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

        self.timer.reset()
        self.timer.start()
        # self.select = self.chooser.getSelected()


    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        while self.isAutonomous() and self.isEnabled():
            # Drive for two seconds
            if self.timer.get() > 0.0 and self.timer.get() < 10.0:
                self.drive.arcadeDrive(0.5, 0)  # Drive forwards at half speed
            else:
                self.drive.arcadeDrive(0, 0)  # Stop robot
            # elif self.timer.get() > 10.0 and self.timer.get() < 11.5:
            #     self.drive.arcadeDrive(0, 0.5 * self.select) # Changes to - for Left side, change to + for Right side
            # elif self.timer.get() > 11.5 and self.timer.get() < 13.0:
                # self.drive.arcadeDrive(-0.5, 0)


    def teleopInit(self):
        """This function is run once each time the robot enters teleop mode"""
        self.kLeft = self.controller.Hand.kLeft
        self.kRight = self.controller.Hand.kRight
        self.lift.set(True) #True makes it fall
        self.timer.reset()
        self.timer.start()




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

            # Drive #
            self.drive.arcadeDrive(self.TriggerLeft, self.controller.getX(self.kLeft))

            # Intake Motors #
            if self.controller.getBButton():
                self.intake.set(1.0)
            elif self.controller.getAButton():
                self.intake.set(-1.0)
            else:
                self.intake.set(0)

            # Loader #
            if self.TriggerRight:
                self.loader.set(wpilib.Relay.Value.kForward)
            elif self.BumperRight:
                self.loader.set(wpilib.Relay.Value.kReverse)
            else:
                self.loader.set(wpilib.Relay.Value.kOff)

            # Ultrasonic #
            # if self.timer.get() >= 2.0:
            #     self.timer.reset()
            #     self.timer.start()
            #     self.table.putNumber('Range In Inches', self.ultrasonic.GetRangeInInches(self))


if __name__ == "__main__":
    wpilib.run(robot,
            physics_enabled=True)
