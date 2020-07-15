Code for the ZED-F9P GNSS Module u-blox GPS Receiver
===================================================
### About
This is the code running the onboard GPS receiver. The receiver is constantly getting navigational data (latitude, longitude, speed, etc) and publishing it through LCM.

### LCM Channels
GPS Data [Publisher]\
Messages: [GPSData.lcm](https://github.com/Polishdudealan/mrover-workspace/blob/master/rover_msgs/GPSData.lcm)\
Publishers: beaglebone/gps

### Usage
Required electrical components: \
1 Antenna \
1 u-blox GPS \
1 Beaglebone green/black

Connect the UART ports on the reveiver and beaglebone together (TXD to RXD and vice versa) and make sure to power the IOREF pin on the receiver with 5.5V otherwise UART will not be enabled. The Beaglebone and receiver also need to be powered. Two USB to USB Micro cables will do the trick. The GPS receiver can also be configured through the GUI (To increase sampling rate for example).

### Building
SSH into the Beaglebone and open up the terminal. Type\
```$ cd ~/mrover-workspace/``` to move to the mrover-workspace directory\
```$ ./jarvis build beaglebone/gps``` to build the gps program\
```$ ./jarvis exec beaglebone_gps``` to run the gps program

### Testing with LCM Echoer
First set up the UART ports.\
```$ python3```\
```>>> import Adafruit_BBIO.UART as UART```\
```>>> UART.setup("UART4")```\
```>>> exit()```

Then in the mrover-workspace directory, type\
```$ sudo ifconfig lo multicast```\
```$ sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev lo```\
in order to setup the network (or optionally set up internet).

To send LCM messages, type\
```$ LCM_DEFAULT_URL="udpm://239.255.76.67:7667?ttl=255" ./jarvis exec beaglebone_gps```

To receive LCM messages, in a *new* window type\
```$ LCM_DEFAULT_URL="udpm://239.255.76.67:7667?ttl=255" ./jarvis exec lcm_tools_echo GPSData /gps_data```\
LCM Messages should start appearing in the new window.

### GUI Info
This GPS also comes with a GUI from u-blox that is fairly easy to setup. It operates with just a USB connection (Make sure the power+gps side is the one plugged in). See resources below for more info.

### NMEA Sentences
NMEA Sentences, or National Marine Electronics Association Sentences, is a data standard that provide satellite data to GPS receivers. There are different types of sentences with different data, configurations, and datatypes. See resources below for more info.

### Debugging
No data will be found if the GPS antenna does not "see" any satellites. For best performance, a clear view of the sky will be needed for the antenna.

### Notes
In receiving LCM messages, "GPSData" might be changed to "GPS" in the future.

### Resources & Data Sheets
[u-blox ZED-F9P GPS Datasheet](https://www.u-blox.com/sites/default/files/ZED-F9P_DataSheet_%28UBX-17051259%29.pdf)\
[GUI Download](https://www.u-blox.com/en/product/u-center)\
[GUI Userguide](https://www.u-blox.com/sites/default/files/u-center_Userguide_%28UBX-13005250%29.pdf)\
[NMEA Sentences guide](https://www.gpsinformation.org/dale/nmea.htm)
