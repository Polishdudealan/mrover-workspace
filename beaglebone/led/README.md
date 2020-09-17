Code for communicating with the NeoPixel NeoMatrix 8x8 - 64 RGB LED Pixel Matrix
===========================================================
### About
This program runs on the beaglebone. It interprets the led lcm struct and sends corresponding commands through UART to an arduino which drives the led board. It sends the following three strings as bytes depending on the command in the lcm struct.
- "A" if the mode is Autonomous
- "M" if the mode is Manual
- "L" if the mode is Leg (once a leg of the autonomous path has been completed)

#### LCM Channels
LED [subscriber]\
Messages: [LEDCmd](https://github.com/Polishdudealan/mrover-workspace/blob/led/rover_msgs/LEDCmd.lcm)\
Publishers: Auton Team\
Subscribers: beaglebone/led


### Usage
Required components:\
1 Beaglebone Black\
1 Arduino Uno\
1 solid-core male-male jumper cable
1 NeoPixel NeoMatrix 8x8 - 64 RGB LED Pixel Matrix

Since the commands will only be going one way, from the BB to the arduino, we only need to connect the BB's transmit UART port to the arduino's Receive UART port. 
You may also want to ground the two devices together but that is optional depending on how they are being powered.

#### Building
SSH into the Beaglebone and open up the terminal. Type\
```$ cd ~/mrover-workspace/``` to move to the mrover-workspace directory\
```$ ./jarvis build beaglebone/led``` to build the led program\
```$ ./jarvis exec beaglebone_led``` to run the led program

#### Exceptions
Currently there is only one exception being looked for, the WriteTimemoutException from the pyserial Write() command. If the exception occurs, an error message will print out to the console.

#### ToDo
- [ ] build and test code on Beaglebone.
- [ ] test code with arduino.
