import serial
import lcm
from rover_msgs import LED
import struct
import Adafruit_BBIO.UART as UART
lcm_ = lcm.LCM()

baud = 9600

def send_data():


def main():
    UART.setup("UART4")
    lmc = LCM()

    with serial.Serial(port="/dev/ttyS4", baudrate=baud) as ser:
        ser.close()
        ser.open()

        while(True):
            if ser.isOpen():
                
                if led.mode = "A":
                    # TODO
                    pass
                elif led.mode = "M":
                    # TODO
                    pass
                elif led.mode = "L":
                    # TODO
                    pass
                else:
                    "Unable to read lcm struct"




def(if __name__ == "__main__"):
    main()