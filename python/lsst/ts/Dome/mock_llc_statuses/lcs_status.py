import logging

from .base_mock_status import BaseMockStatus
from ..llc_status import LlcStatus


class LcsStatus(BaseMockStatus):
    """Represents the status of the Louvers Control System in simulation mode.
    """

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger("MockLcsStatus")
        # variables holding the status of the mock Louvres
        self.status = [LlcStatus.CLOSED.value] * 34
        self.position_error = [0.0] * 34
        self.position_actual = [0.0] * 34
        self.position_cmd = [0.0] * 34
        self.drive_torque_actual = [0.0] * 68
        self.drive_torque_error = [0.0] * 68
        self.drive_torque_cmd = [0.0] * 68
        self.drive_current_actual = [0.0] * 68
        self.drive_temp_actual = [20.0] * 68
        self.encoder_head_raw = [0.0] * 68
        self.encoder_head_calibrated = [0.0] * 68
        self.power_absortion = 0.0

    async def determine_status(self):
        """Determine the status of the Lower Level Component and store it in the llc_status `dict`.
        """
        self.llc_status = {
            "status": self.status,
            "positionError": self.position_error,
            "positionActual": self.position_actual,
            "positionCmd": self.position_cmd,
            "driveTorqueActual": self.drive_torque_actual,
            "driveTorqueError": self.drive_torque_error,
            "driveTorqueCmd": self.drive_torque_cmd,
            "driveCurrentActual": self.drive_current_actual,
            "driveTempActual": self.drive_temp_actual,
            "encoderHeadRaw": self.encoder_head_raw,
            "encoderHeadCalibrated": self.encoder_head_calibrated,
            "powerAbsortion": self.power_absortion,
        }
        self.log.debug(f"lcs_state = {self.llc_status}")

    async def setLouver(self, louver_id, position):
        """Mock setting the position of the louver with the given louver_id.

        Parameters
        ----------
        louver_id: `int`
            The ID of the louver to set the position for. A zero based ID is assumed.
        position: `int`
            The position (deg) to set the louver to. 0 means closed, 180 means wide open. These limits are
            not checked.
        """
        # TODO Make sure that radians are used because that is what the real LLCs will use as well. DM-24789
        self.status[louver_id] = LlcStatus.OPEN.value
        self.position_actual[louver_id] = position
        self.position_cmd[louver_id] = position

    async def closeLouvers(self):
        self.status = [LlcStatus.CLOSED.value] * 34
        self.position_actual = [0.0] * 34
        self.position_cmd = [0.0] * 34

    async def stopLouvers(self):
        """Mock stopping all motion of all louvers.
        """
        self.status = [LlcStatus.STOPPED.value] * 34
