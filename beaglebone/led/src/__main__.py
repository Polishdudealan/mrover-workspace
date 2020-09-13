import serial
import lcm
from rover_msgs import LED
import struct
import Adafruit_BBIO.UART as UART
lcm_ = lcm.LCM()

baud = 9600

def main():
    UART.setup("UART4")
    led = LED()

    with serial.Serial(port="/dev/ttyS4", baudrate=baud) as ser:
        ser.close()
        ser.open()

        while(True):
            if ser.isOpen():
                try:
                    if led.mode == "A":
                        ser.write("A".encode('utf-8'))
                    elif led.mode == "M":
                        ser.write("M".encode('utf-8'))
                    elif led.mode == "L":
                        ser.write("L".encode('utf-8'))
                    else:
                        print("Unable to read lcm struct")
                except ser.SerialTimeoutException:
                    print("write timeout")
            else:
                print("Serial is not open")


if __name__ == "__main__":
    main()