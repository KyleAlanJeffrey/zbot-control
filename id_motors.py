#!/usr/bin/env python
#
# *********     Ping Example      *********
#
#
# Available SC Servo model on this example : All models using Protocol SC
# This example is tested with a SC15/SC09 Servo, and an URT
#

import sys
import os

from scservo_sdk import *  # Uses SC Servo SDK library

# Default setting
BAUDRATE = 1000000  # SC Servo default baudrate : 1000000
DEVICENAME = (
    "/dev/tty.usbmodem58FA0833071"  # Check which port is being used on your controller
)
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

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
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Try to ping the SC Servo
# Get SC Servo model number
for i in range(255):
    scs_model_number, scs_comm_result, scs_error = packetHandler.ping(i)
    if scs_comm_result != COMM_SUCCESS:
        print(".", end="")
        sys.stdout.flush()
        continue
    else:
        print(
            "\n[ID:%03d] ping Succeeded. SC Servo model number : %d"
            % (i, scs_model_number)
        )
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))

# Close port
portHandler.closePort()
