#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available ST Servo model on this example : All models using Protocol ST
# This example is tested with a ST Servo(ST3215/ST3020/ST3025), and an URT
#

# SERVOS ARE 31-45
# SERVOS ARE 41-45

import sys
import os
from scservo_sdk import *  # Uses SC Servo SDK library

import sys, tty, termios

# LEFT_LEG_IDS = [31, 32, 33, 34, 35]
LEFT_LEG_IDS = []
RIGHT_LEG_IDS = [41, 42, 43, 44, 45]

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
    print("Press any key to terminate...")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()

while 1:
    input("Press Enter to move all servos to neutral position...")

    for SCS_ID in LEFT_LEG_IDS + RIGHT_LEG_IDS:
        neutral_position = (
            SCS_MINIMUM_POSITION_VALUE + SCS_MAXIMUM_POSITION_VALUE
        ) // 2

        # Write SC Servo goal position/moving speed/moving acc
        scs_comm_result, scs_error = packetHandler.WritePosEx(
            SCS_ID, neutral_position, SCS_MOVING_SPEED, SCS_MOVING_ACC
        )
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
        input(
            "Moved servo ID %d to neutral position. Press Enter to continue..." % SCS_ID
        )

# Close port
portHandler.closePort()
