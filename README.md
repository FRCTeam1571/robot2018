This is the code for 1571's 2018 robot. Made by [@trevor34](https://github.com/trevor34)

How to deploy:
- Open command prompt
- Type `cd c:/path/to/file`
- Type `py robot.py --skip-tests`
- Open driverstation software
- Wait for both communications and robot code light to go green

How to run pneumatics:
- Connect the wires to pneumatic compressor
- Select Test mode in the driverstation and enable
- Wait for the pneumatic compressor to shut off and disable the driverstation
- Have someone hold the arms on the robot in up
- Press the orange button on the pneumatic solenoid labeled '1'. The cylinder should pop up, so stay clear
- Reenable the robot in Test mode to fill up the pneumatics
- Disable robot and disconnect pneumatic compressor
- The cylinder should go down at the start of Teleop mode

Autonomous:
- Drives forward for 5 seconds

Teleop controls:
- Left Trigger - Forward
- Left Bumper + Left Trigger - Reverse
- B button - Intake motors in
- Y button - Intake motors out
- A button - Lift
- X button - Grabber toggle
- Right Bumper - Relay forward
- Right Trigger - Relay back

