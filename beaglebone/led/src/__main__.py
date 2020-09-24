import serial
import lcm
from rover_msgs import AutonState, NavStatus
import Adafruit_BBIO.UART as UART
lcm_ = lcm.LCM()

baud = 9600


def nav_status_callback(channel, msg):
    status = NavStatus.decode(msg)
    with serial.Serial(port="/dev/ttyS4", baudrate=baud) as ser:
        if ser.isOpen():
            try:
                if status.nav_state_name == "A":
                    ser.write("A".encode('utf-8'))
                elif status.nav_state_name == "M":
                    ser.write("M".encode('utf-8'))
                elif status.nav_state_name == "Done":
                    ser.write("D".encode('utf-8'))
                else:
                    print("Unable to read lcm struct")
            except ser.SerialTimeoutException:
                print("write timeout")
        else:
            print("Serial is not open")


def auton_state_callback(channel, msg):
    state = AutonState.decode(msg)
    if(state.is_auton):
        lcm_.subscribe("/NavStatus", nav_status_callback)


def main():
    lcm_.subscribe("/AutonState", auton_state_callback)
    UART.setup("UART4")
    with serial.Serial(port="/dev/ttyS4", baudrate=baud) as ser:
        ser.close()
        ser.open()

        while(True):
            lcm_.handle()


if __name__ == "__main__":
    main()
