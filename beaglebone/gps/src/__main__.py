import serial
import lcm
from rover_msgs import GPS
import struct
import numpy as np
import Adafruit_BBIO.UART as UART
lcm_ = lcm.LCM()

baud = 38400


def main():
    # Setup UART ports
    UART.setup("UART4")

    gps = GPS()
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
            # reads in data as a string and formats it into a list
            data = str(ser.read_until())
            datastring = data[2:-1]
            datalist = datastring.split(',')
            if(datalist[0] == "$GNRMC"):
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
                        gps.latitude_min = (float(datalist[3]) % 100) * -1.0
                        gps.latitudeDirection = "S"
                else:
                    gps.latitude_deg = 0
                    gps.latitude_min = 0
                    gps.latitudeDirection = "-"
                if(datalist[5] != ""):
                    if(datalist[6] == "W"):
                        gps.longitude_deg = np.int16(int(float(datalist[5]) / 100) * -1.0)
                        gps.longitude_min = (float(datalist[5]) % 100) * -1.0
                        gps.longitudeDirection = "W"
                    elif(datalist[6] == "E"):
                        gps.longitude_deg = np.int16(int(float(datalist[5]) / 100))
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
                # km/h
                if(datalist[7] != ""):
                    gps.speed_kmh = float(datalist[7])
                else:
                    gps.speed_kmh = 0
            elif(datalist[0] == "$GNGGA"):
                # 0-8
                if(datalist[6] != ""):
                    gps.quality = int(datalist[6], 10)
                else:
                    gps.quality = 0
            if(tempTimeStamp != gps.timeStamp):
                # publishes data
                lcm_.publish('/gps_data', gps.encode())
                tempTimeStamp = gps.timeStamp


if (__name__ == "__main__"):
    main()
