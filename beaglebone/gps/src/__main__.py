import serial
# import string
import lcm
from rover_msgs import GPSData
import struct
lcm_ = lcm.LCM()

baud = 38400


def main():

    gps = GPSData()
    tempTimeStamp = 0
    # default frequency of data collection
    milliseconds = 40
    # hex converted to int to satisfy python gods
    keyId = 807469057
    frequencyBytes = struct.pack(">h", milliseconds)
    commandBytes = struct.pack(">I", keyId)
    with serial.Serial(port="/dev/ttyS4", bytesize=serial.EIGHTBITS,
                       stopbits=serial.STOPBITS_ONE,
                       parity=serial.PARITY_NONE, xonxoff=False, rtscts=False,
                       dsrdtr=False, baudrate=baud) as ser:
        ser.write(commandBytes)
        ser.write(frequencyBytes)
        while(True):
            # reads in data as a string
            data = str(ser.read_until())
            # removes extra quotes around the data string
            datastring = data[2:-1]

            # splits up correctly formatted string into a list of strings
            datalist = datastring.split(',')
            # print("datalist is of type: ", type(datalist), "size is: ",
            # len(datalist))
            if(datalist[0] == "$GNRMC"):
                #  print("Transmission Type:", datalist[0], "timeStamp:",
                # datalist[1],
                # "Status (A=active, V = void):", datalist[2],
                # "Latitude:", datalist[3], ",", datalist[4], "Longitude:",
                # datalist[5],
                # ",", datalist[6], "Ground speed(knots):", datalist[7],
                # "Track angle(in Degrees True):", datalist[8])

                # time
                if(datalist[1] != ""):
                    gps.timeStamp = float(datalist[1])
                else:
                    gps.timeStamp = tempTimeStamp
                # dddmm.mmmm format (degrees, minutes, minutes/seconds
                if(datalist[3] != ""):
                    if(datalist[4] == "N"):
                        gps.latitude_deg = int(float(datalist[3]) / 100)
                        gps.latitude_min = float(datalist[3]) % 100
                    elif(datalist[4] == "S"):
                        gps.latitude_deg = int(float(datalist[3]) / 100) * -1.0
                        gps.latitude_min = float(datalist[3]) % 100
                else:
                    gps.latitude_deg = 0
                    gps.latitude_min = 0
                if(datalist[5] != ""):
                    if(datalist[6] == "W"):
                        gps.longitude_deg = int(float(datalist[5]) / 100)
                        gps.longitude_min = float(datalist[5]) % 100
                    elif(datalist[6] == "E"):
                        gps.longitude_deg = int(float(datalist[5]) / 100) * -1
                        gps.longitude_min = float(datalist[5]) % 100
                else:
                    gps.longitude_deg = 0
                    gps.longitude_min = 0
                if(datalist[8] != ''):
                    # degrees
                    gps.bearing_deg = float(datalist[8])
                else:
                    # degrees
                    gps.bearing_deg = 0

            elif(datalist[0] == "$GNVTG"):
                # print("Transmission Type:", datalist[0],
                # "True track made good:", datalist[1],
                # "Magnetic track:", datalist[2], "Ground speed(knots):",
                # datalist[3],
                # "Ground speed(km/h):", datalist[7])

                # km/h
                if(datalist[7] != ""):
                    gps.speed = float(datalist[7])
                else:
                    gps.speed = 0
            elif(datalist[0] == "$GNGGA"):
                # print("Transmission Type:", datalist[0],
                # "Fix Quality(4=RTK):", datalist[6],
                # "Number of satellites tracked:", datalist[7],
                # "Altitude (above mean sea level):", datalist[9],
                # "time since last DGPS update (s):", datalist[11])

                # 0-4
                if(datalist[6] != ""):
                    gps.quality = int(datalist[6], 10)
                else:
                    gps.quality = 0

                # mean sea level altitude in meters
                if(datalist[9] != ""):
                    gps.altitude = float(datalist[9])
                else:
                    gps.altitude = 0
            elif(datalist[0] == "$GPGSV"):
                # print("Transmission Type:", datalist[0],
                # "# of sentences for full data:", datalist[1],
                # "Sentence _ of total:", datalist[2],
                # "# satellites in view:", datalist[3]

                # int
                if(datalist[3] != ""):
                    gps.satellitesInView = int(datalist[3], 10)
                else:
                    gps.satellitesInView = 0
            if(tempTimeStamp != gps.timeStamp):
                # publishes data
                lcm_.publish('/gps_data', gps.encode())
                tempTimeStamp = gps.timeStamp


if (__name__ == "__main__"):
    main()
