from loguru import logger

from scservo_sdk.scservo_def import COMM_SUCCESS


def comm_error_log(comm_result, error, packet_handler):
    """Logs communication errors for motor actions."""
    if comm_result != COMM_SUCCESS:
        logger.error(
            f"Failed {packet_handler.getTxRxResult(comm_result)}"
        )
    if error != 0:
        logger.error(
            f"Error : {packet_handler.getRxPacketError(error)}"
        )