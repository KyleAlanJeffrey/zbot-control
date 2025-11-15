#!/usr/bin/env python

# SERVOS ARE 31-45
# SERVOS ARE 41-45

import argparse

from scservo_sdk import *  # Uses SC Servo SDK library

# Default setting
BAUDRATE = 1000000  # SC Servo default baudrate : 1000000
DEVICENAME = (
    "/dev/cu.usbmodem58FA0833071"  # Check which port is being used on your controller
)
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
SCS_MINIMUM_POSITION_VALUE = 0  # SC Servo will rotate between this value
SCS_MAXIMUM_POSITION_VALUE = 4095
SCS_MOVING_SPEED = 800  # SC Servo moving speed
SCS_MOVING_ACC = 25  # SC Servo moving acc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Usage: python move_motor.py <id> --position-deg <deg>"
    )
    parser.add_argument("motor_id", help="ID of the motor to test", type=int)
    parser.add_argument(
        "--position-deg", help="Position to move the motor to", type=int, required=True
    )
    args = parser.parse_args()

    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Get methods and members of Protocol
    packetHandler = sms_sts(portHandler)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        quit()

    # map degree position to servo position value
    position = int(((args.position_deg % 359) / 360) * SCS_MAXIMUM_POSITION_VALUE)
    print(f"Sending motor to position -> {position} - {args.position_deg}")
    # Write SC Servo goal position/moving speed/moving acc
    scs_comm_result, scs_error = packetHandler.WritePosEx(
        args.motor_id, position, SCS_MOVING_SPEED, SCS_MOVING_ACC
    )
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))

    # Close port
    portHandler.closePort()
