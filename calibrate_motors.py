#!/usr/bin/env python
#
# *********     Ping Example      *********
#
#
# Available SC Servo model on this example : All models using Protocol SC
# This example is tested with a SC15/SC09 Servo, and an URT
#

import argparse
import sys

from buster.motors import MotorCommunicator
from buster.scservo_sdk.scservo_def import COMM_SUCCESS

MIN_VOLTAGE = 40
MAX_VOLTAGE = 140
MAX_TEMPERATURE = 70

DEVICENAME = (
    "/dev/tty.usbmodem58FA0833071"  # Check which port is being used on your controller
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Usage: python calibrate_motors.py --read_only"
    )
    parser.add_argument("--read_only", help="Run the script in read-only mode", action="store_true")
    args = parser.parse_args()

    motor_comms = MotorCommunicator(device_name=DEVICENAME)

    # Try to ping the SC Servo
    # Get SC Servo model number
    for motor_id in range(255):
        if not motor_comms.is_online(motor_id):
            print(".", end="")
            sys.stdout.flush()
            continue

        motor_state = motor_comms.get_motor_state(motor_id)
        print(motor_state)

        if args.read_only:
            continue

        ##### Set Voltage Limits #####
        print("Setting Voltage Limits to %.2f V - %.2f V" % (MIN_VOLTAGE / 10.0, MAX_VOLTAGE / 10.0))
        comm_result, error = motor_comms.packet_handler.WriteVoltageLimits(motor_id, MAX_VOLTAGE, MIN_VOLTAGE)

        #### Set Temperature Limits #####
        print("Setting Max Temperature Limit to %.2f C" % (MAX_TEMPERATURE))
        comm_result, error = motor_comms.packet_handler.WriteTemperatureLimit(motor_id, MAX_TEMPERATURE)

    motor_comms.close()




            # ##### Voltage Limits #####
            # voltage, scs_comm_result, scs_error = packetHandler.ReadVoltage(i)
            # max_voltage, min_voltage, scs_comm_result, scs_error = packetHandler.ReadVoltageLimits(i)
            # print(
            #     "[ID:%03d] Voltage : %.2f V (Min: %.2f V, Max: %.2f V)"
            #     % (i, voltage / 10.0, min_voltage / 10.0, max_voltage / 10.0)
            # )
            # ##### Temperature Limits #####
            # max_temp, scs_comm_result, scs_error = packetHandler.ReadTemperatureLimit(i)
            # print("[ID:%03d] Max Temperature Limit : %.2f C" % (i, max_temp))

            # ##### Motor angle limits #####
            # # Current angle
            # pos, scs_comm_result, scs_error = packetHandler.ReadPos(i)
            # print("[ID:%03d] Current Position : %d" % (i, pos))
            # min_angle, max_angle, scs_comm_result, scs_error = packetHandler.ReadMotorLimits(i)
            # print("[ID:%03d] Motor Angle Limits : Min %d, Max %d" % (i, min_angle, max_angle))

