from dataclasses import dataclass
from typing import Dict, List, Optional
from loguru import logger
from .scservo_sdk.scservo_def import COMM_SUCCESS
from .scservo_sdk.sms_sts import sms_sts
from .scservo_sdk.port_handler import PortHandler

# Default setting
BAUDRATE = 1000000  # SC Servo default baudrate : 1000000
DEVICENAME = (
    "/dev/tty.usbmodem58FA0833071"  # Check which port is being used on your controller
)
SCS_MINIMUM_POSITION_VALUE = 0  # SC Servo will rotate between this value
SCS_MAXIMUM_POSITION_VALUE = 4095
SCS_MOVING_SPEED = 800  # SC Servo moving speed
SCS_MOVING_ACC = 25  # SC Servo moving acc


@dataclass
class MotorState:
    id: int
    model_number: int
    min_voltage_limit: float
    max_voltage_limit: float
    max_temperature: float
    min_angle_limit: int
    max_angle_limit: int
    current_position: int
    current_temperature: float
    current_voltage: float

    def __repr__(self):
        return (
            f"\nMotor - #{self.id} | Model #{self.model_number}\n"
            f"--------------------------\n"
            f" Position:    {self.current_position} - [{self.min_angle_limit}, {self.max_angle_limit}]\n"
            f" Voltage:     {self.current_voltage} V - [{self.min_voltage_limit}, {self.max_voltage_limit}]\n"
            f" Temperature: {self.current_temperature}/{self.max_temperature} C"
        )


class MotorCommunicator:
    def __init__(self, device_name=DEVICENAME, baud_rate=BAUDRATE):
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        port_handler = PortHandler(device_name)

        try:
            success = port_handler.openPort()
            if not success:
                raise RuntimeError(f"Failed to open the port for {device_name}")
        except Exception as e:
            raise RuntimeError(f"Failed to open port for {device_name}")

        try:
            success = port_handler.setBaudRate(baud_rate)
        except Exception as e:
            raise RuntimeError(f"Failed to set baudrate to {baud_rate}")

        # Initialize PacketHandler instance
        self.packet_handler = sms_sts(port_handler)
        logger.info(
            f"MotorCommunicator initialized on {device_name} at {baud_rate} baud."
        )

    def is_online(self, motor_id: int) -> bool:
        """Ping the motor to check if it's responsive."""
        _, comm_result, _ = self.packet_handler.ping(motor_id)
        return comm_result == COMM_SUCCESS

    def get_motor_state(self, motor_id: int) -> Optional[MotorState]:
        """Ping the motor and retrieve its state. Returns None if ping fails."""
        model_number, comm_result, error = self.packet_handler.ping(motor_id)
        if comm_result != COMM_SUCCESS:
            logger.warning(f"Ping failed for motor ID {motor_id}")
            return None

        voltage, comm_result, error = self.packet_handler.ReadVoltage(motor_id)
        max_voltage, min_voltage, comm_result, error = (
            self.packet_handler.ReadVoltageLimits(motor_id)
        )
        max_temp, comm_result, error = self.packet_handler.ReadTemperatureLimit(
            motor_id
        )
        temp, comm_result, error = self.packet_handler.ReadTemperature(motor_id)
        pos, comm_result, error = self.packet_handler.ReadPos(motor_id)
        min_angle, max_angle, comm_result, error = self.packet_handler.ReadMotorLimits(
            motor_id
        )

        return MotorState(
            id=motor_id,
            model_number=model_number,
            min_voltage_limit=min_voltage / 10.0,
            max_voltage_limit=max_voltage / 10.0,
            max_temperature=max_temp,
            min_angle_limit=min_angle,
            max_angle_limit=max_angle,
            current_position=pos,
            current_temperature=temp,
            current_voltage=voltage / 10.0,
        )

    def get_motor_positions(self, motor_ids: List[int]) -> Dict[int, int]:
        """Get current positions of multiple motors."""
        positions = {}
        for motor_id in motor_ids:
            pos, comm_result, error = self.packet_handler.ReadPos(motor_id)
            if comm_result != COMM_SUCCESS:
                logger.error(
                    f"Failed to read position from motor ID {motor_id}: {error}"
                )
                continue
            positions[motor_id] = pos
        return positions

    def send_motor_positions(
        self,
        positions: Dict[int, int],
        speed: int = SCS_MOVING_SPEED,
        acc: int = SCS_MOVING_ACC,
    ) -> None:
        """Send position commands to multiple motors."""
        for motor_id, position in positions.items():
            logger.debug(
                f"Sending position {position} to motor ID {motor_id} with speed {speed} and acc {acc}"
            )
            comm_result, error = self.packet_handler.WritePosEx(
                motor_id, position, speed, acc
            )

            if comm_result != COMM_SUCCESS:
                err = f"{self.packet_handler.getTxRxResult(comm_result)}"
                logger.error(
                    f"Failed to send position to motor ID {motor_id}: {err}"
                )
            if error != 0:
                err = f"{self.packet_handler.getRxPacketError(error)}"
                logger.error(
                    f"Error from motor ID {motor_id} after sending position: {err}"
                )

    def close(self):
        """Close the port handler."""
        self.packet_handler.portHandler.closePort()
