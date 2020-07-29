import serial
import lcm
from rover_msgs import GPSData
import struct
import numpy as np
lcm_ = lcm.LCM()

baud = 38400


def main():

    gps = GPSData()
    tempTimeStamp = 0
    # 4 byte code for the register where cfg-rate is located
    header1 = 181
    header2 = 98
    classId = 6
    Id = 8
    # message size (bytes)
    payloadSize = 6
    # frequency of data collection
    milliseconds = 50
    # number of measurements per solution
    navRatio = 1
    # time reference (UTC, GPS, etc)
    timeRef = 1
    # byteOffset
    byteOffset = 0

    # This block changes above constants int bytes or shorts
    comBytes1 = struct.pack("<B", header1)
    comBytes2 = struct.pack("<b", header2)
    frequencyBytes = struct.pack(">h", milliseconds)
    navRatioBytes = struct.pack(">h", navRatio)
    timeRefBytes = struct.pack(">h", timeRef)

    # Calculating checksum
    Buffer = [classId, Id, payloadSize, frequencyBytes[0], frequencyBytes[1],
              navRatioBytes[0], navRatioBytes[1], timeRefBytes[0],
              timeRefBytes[1], byteOffset]
    ck_a = 0
    ck_b = 0
    for i in range(10):
        ck_a = ck_a + Buffer[i]
        ck_b = ck_b + ck_a
    # bitmasking (in equation in doc sheet)
    ck_a = ck_a & 0xFF
    ck_b = ck_b & 0xFF

    ck_aBytes = struct.pack("<b", ck_a)
    ck_bBytes = struct.pack("<B", ck_b)

    with serial.Serial(port="/dev/ttyS4", bytesize=serial.EIGHTBITS,
                       stopbits=serial.STOPBITS_ONE,
                       parity=serial.PARITY_NONE, xonxoff=False, rtscts=False,
                       dsrdtr=False, baudrate=baud) as ser:

        # writes a 14 byte command specifically to the cfg-rate settings
        ser.write(comBytes1)
        ser.write(comBytes2)
        ser.write(bytearray(Buffer))
        ser.write(ck_aBytes)
        ser.write(ck_bBytes)

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
                        gps.latitude_deg = np.int16(int(float(datalist[3]) / 100))
                        gps.latitude_min = float(datalist[3]) % 100
                        gps.latitudeDirection = "N"
                    elif(datalist[4] == "S"):
                        gps.latitude_deg = np.int16(int(float(datalist[3]) / 100) * -1.0)
                        gps.latitude_min = float(datalist[3]) % 100
                        gps.latitudeDirection = "S"
                else:
                    gps.latitude_deg = 0
                    gps.latitude_min = 0
                    gps.latitudeDirection = "-"
                if(datalist[5] != ""):
                    if(datalist[6] == "W"):
                        gps.longitude_deg = np.int16(int(float(datalist[5]) / 100))
                        gps.longitude_min = float(datalist[5]) % 100
                        gps.longitudeDirection = "W"
                    elif(datalist[6] == "E"):
                        gps.longitude_deg = np.int16(int(float(datalist[5]) / 100) * -1.0)
                        gps.longitude_min = float(datalist[5]) % 100
                        gps.longitudeDirection = "E"
                else:
                    gps.longitude_deg = 0
                    gps.longitude_min = 0
                    gps.longitudeDirection = "-"
                if(datalist[8] != ''):
                    # degrees
                    gps.trackAngle_deg = float(datalist[8])
                else:
                    # degrees
                    gps.trackAngle_deg = 0

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
            # elif(datalist[0] == "$GNGGA"):
                # print("Transmission Type:", datalist[0],
                # "Fix Quality(4=RTK):", datalist[6],
                # "Number of satellites tracked:", datalist[7],
                # "Altitude (above mean sea level):", datalist[9],
                # "time since last DGPS update (s):", datalist[11])
                # 0-4
                # if(datalist[6] != ""):
                    # gps.quality = int(datalist[6], 10)
                # else:
                    # gps.quality = 0

                # mean sea level altitude in meters
                # if(datalist[9] != ""):
                    # gps.altitude = float(datalist[9])
                # else:
                    # gps.altitude = 0
            # elif(datalist[0] == "$GPGSV"):
                # print("Transmission Type:", datalist[0],
                # "# of sentences for full data:", datalist[1],
                # "Sentence _ of total:", datalist[2],
                # "# satellites in view:", datalist[3]

                # int
                # if(datalist[3] != ""):
                    # gps.satellitesInView = int(datalist[3], 10)
                # else:
                    # gps.satellitesInView = 0
            if(tempTimeStamp != gps.timeStamp):
                # publishes data
                # print("tempTime:", tempTimeStamp, "tStamp:", gps.timeStamp)
                lcm_.publish('/gps_data', gps.encode())
                tempTimeStamp = gps.timeStamp


if (__name__ == "__main__"):
    main()
