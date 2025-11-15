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
    parser = argparse.ArgumentParser(description="Motor Tester script. Usage")
    parser.add_argument("motor_id", help="ID of the motor to test", type=int)
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

    # Move the motor back and forth increasing by increments of 100
    increment = 100
    position = SCS_MINIMUM_POSITION_VALUE
    cycles = 2
    print("Moving motor ID %d back and forth" % args.motor_id)
    while True:
        position += increment
        print("Goal Position : %d " % position)
        if position >= SCS_MAXIMUM_POSITION_VALUE:
            position = SCS_MAXIMUM_POSITION_VALUE
            increment = -increment
            cycles -= 1
        elif position <= SCS_MINIMUM_POSITION_VALUE:
            position = SCS_MINIMUM_POSITION_VALUE
            increment = -increment
            cycles -= 1

        if cycles <= 0:
            break

        # Write SC Servo goal position/moving speed/moving acc
        scs_comm_result, scs_error = packetHandler.WritePosEx(
            args.motor_id, position, SCS_MOVING_SPEED, SCS_MOVING_ACC
        )
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))

        time.sleep(0.5)

        # # Wait until the SC Servo reaches the goal position
        # while True:
        #     # Read SC Servo present position
        #     scs_present_position, scs_comm_result, scs_error = packetHandler.ReadPos(
        #         args.motor_id
        #     )
        #     if scs_comm_result != COMM_SUCCESS:
        #         print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        #     if scs_error != 0:
        #         print("%s" % packetHandler.getRxPacketError(scs_error))

        #     print("  PresPos:%d" % scs_present_position)

        #     if not (abs(position - scs_present_position) > 10):
        #         break

    # Close port
    portHandler.closePort()
