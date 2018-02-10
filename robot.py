
#!/usr/bin/env python3

import wpilib
from wpilib import drive, timer
import ctre
# from networktables import NetworkTables


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

        self.lift = wpilib.Solenoid(0, 0)
        self.grab = wpilib.Solenoid(0, 1)


        # self.rr_motor.set(mode(Follower))
        # self.rr_motor.set(self.fr_motor.getDeviceID())
        # self.rl_motor.set(mode(Follower))
        # self.rl_motor.set(self.fl_motor.getDeviceID())



        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.wpilib.Timer.reset()
        self.wpilib.Timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        while self.isAutonomous() and self.isEnabled():
            # Drive for two seconds
            if self.Timer.get() < 2.0:
                self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
            else:
                self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopInit(self):
        """This function is run once each time the robot enters telepo mode"""
        self.kLeft = self.controller.Hand.kLeft
        self.kRight = self.controller.Hand.kRight
        self.lift.set(False)
        self.grab.set(False)
        self.LiftToggle = False
        self.GrabToggle = False
        self.GrabLast = False




    def teleopPeriodic(self):
        # self.lock = 0
        # def axisoutput(numx, numy):
        #     if self.lock == 0:
        #         self.lock = 1
        #         print(numx, numy)
        #         time.sleep(2.5)
        #         self.lock = 0
        #     return
        """This function is called periodically during operator control."""
        while self.isOperatorControl() and self.isEnabled():

            self.TriggerLeft = self.controller.getTriggerAxis(self.kLeft)
            self.TriggerRight = self.controller.getTriggerAxis(self.kRight)
            self.BumperLeft = self.controller.getBumper(self.kLeft)
            self.BumperRight = self.controller.getBumper(self.kRight)
            # self.lAxis = self.controller.getRawAxis(2)
            # self.rAxis = self.controller.getRawAxis(3)
            # # print(self.controller.getMagnitude())
            # threads = []
            # t = threading.Thread(target=axisoutput, args=(self.lAxis, self.rAxis))
            # threads.append(t)
            # t.start()

            # backwards control
            if self.BumperLeft:
                self.TriggerLeft = self.TriggerLeft * -1


            if self.BumperRight:
                self.TriggerRight = self.TriggerRight * -1

            # Drive
            self.drive.arcadeDrive(self.TriggerLeft, self.controller.getX(self.kLeft))

            # Solenoids

            if self.controller.getAButtonPressed() and self.lift.get() == False:
                self.lift.set(True)
            elif self.controller.getAButtonReleased() and self.lift.get() == True:
                self.lift.set(False)

            if self.controller.getXButton() and not self.GrabLast:
                self.GrabToggle = not self.GrabToggle
                # self.GrabLast = True
            # elif self.controller.getXButton() and self.GrabToggle and self.GrabLast == True:
            #     # self.grab.set(False)
            #     self.GrabToggle = False
            #     self.GrabLast = False

            self.GrabLast = self.controller.getXButton()


            if self.GrabToggle and self.GrabLast:
                self.grab.set(True)
            elif self.GrabLast:
                self.grab.set(False)








if __name__ == "__main__":
    wpilib.run(robot,
            physics_enabled=True)
