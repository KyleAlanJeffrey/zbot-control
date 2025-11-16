import argparse
from scservo_sdk import *

# Default setting
BAUDRATE = 1000000  # SC Servo default baudrate : 1000000
DEVICENAME = "/dev/tty.usbmodem58FA0833071"  # Check which port is being used on your controller  # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Usage: python change_id.py <id> <new_id>"
    )
    parser.add_argument("motor_id", help="ID of the motor to test", type=int)
    parser.add_argument("new_motor_id", help="Position to move the motor to", type=int)
    args = parser.parse_args()

    print(f"Changing ID of motor {args.motor_id} to {args.new_motor_id}")

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
        print("Succeeded to set the baudrate")
    else:
        print("Failed to set the baudrate")
        portHandler.closePort()
        quit()

    scs_comm_result, scs_error = packetHandler.unLockEprom(args.motor_id)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    elif scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
        quit()

    scs_comm_result, scs_error = packetHandler.write1ByteTxRx(
        args.motor_id, scs_id, args.new_motor_id
    )
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    else:
        packetHandler.LockEprom(args.motor_id)
        print("Succeeded to change the Servo ID")
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
        quit()
