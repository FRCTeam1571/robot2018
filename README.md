This is the code for 1571's 2018 robot. Made by [@trevor34](https://github.com/trevor34)

How to deploy:
- Attach USB type A to type B cable to RoboRIO and the computer and turn on robot
  - Alternatively you can use an Ethernet cable attached to the robot's radio. But do keep in mind, it takes longer to connect
- Open driverstation software and wait for communications light to go green
- Open command prompt
- Type `cd c:/path/to/directory`
- Type `py robot.py deploy --skip-tests`
  - You may also need to change the IP to the robot. Type `--robot <ip address>` at the end of the command


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
- Drives forward for 10 seconds

Teleop controls:
- Left Trigger - Forward
- Left Bumper + Left Trigger - Reverse
- B button - Intake motors in
- A button - Intake motors out
- X button - Grabber toggle
- Right Bumper - Relay forward
- Right Trigger - Relay back
