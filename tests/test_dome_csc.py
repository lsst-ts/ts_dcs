import asynctest
import logging
import unittest

from lsst.ts import salobj
from lsst.ts import Dome

STD_TIMEOUT = 2  # standard command timeout (sec)

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", level=logging.INFO
)


class CscTestCase(salobj.BaseCscTestCase, asynctest.TestCase):
    def basic_make_csc(self, initial_state, config_dir, simulation_mode, **kwargs):
        return Dome.DomeCsc(
            initial_state=initial_state,
            config_dir=config_dir,
            simulation_mode=simulation_mode,
            mock_port=0,
        )

    async def test_standard_state_transitions(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await self.check_standard_state_transitions(
                enabled_commands=(
                    "moveAz",
                    "moveEl",
                    "stopAz",
                    "stopEl",
                    "stop",
                    "crawlAz",
                    "crawlEl",
                    "setLouver",
                    "closeLouvers",
                    "stopLouvers",
                    "openShutter",
                    "closeShutter",
                    "stopShutter",
                    "park",
                    "setTemperature",
                ),
            )

    async def test_do_moveAz(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_azimuth = 40
            await self.remote.cmd_moveAz.set_start(
                azimuth=desired_azimuth, timeout=STD_TIMEOUT
            )

    async def test_do_moveEl(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_elevation = 40
            await self.remote.cmd_moveEl.set_start(
                elevation=desired_elevation, timeout=STD_TIMEOUT
            )

    async def test_do_stopAz(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_stopAz.set_start()

    async def test_do_stopEl(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_stopEl.set_start()

    async def test_do_stop(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_stop.set_start()

    async def test_do_crawlAz(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_direction = Dome.AzcsMotionDirection.CW.value
            desired_velocity = 0.1
            await self.remote.cmd_crawlAz.set_start(
                dirMotion=desired_direction,
                azRate=desired_velocity,
                timeout=STD_TIMEOUT,
            )

    async def test_do_crawlEl(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_direction = Dome.LwcsMotionDirection.UP.value
            desired_velocity = 0.1
            await self.remote.cmd_crawlEl.set_start(
                dirMotion=desired_direction,
                elRate=desired_velocity,
                timeout=STD_TIMEOUT,
            )

    async def test_do_setLouver(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_id = 5
            desired_position = 60
            await self.remote.cmd_setLouver.set_start(
                id=desired_id, position=desired_position, timeout=STD_TIMEOUT,
            )

    async def test_do_closeLouvers(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_closeLouvers.set_start()

    async def test_do_stopLouvers(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_stopLouvers.set_start()

    async def test_do_openShutter(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_openShutter.set_start()

    async def test_do_closeShutter(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_closeShutter.set_start()

    async def test_do_stopShutter(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_stopShutter.set_start()

    async def test_do_park(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.remote.cmd_park.set_start()

    async def test_do_setTemperature(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            desired_temperature = 10.0
            await self.remote.cmd_setTemperature.set_start(
                temperature=desired_temperature, timeout=STD_TIMEOUT,
            )

    async def test_config(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1,
        ):
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )

            # All values are below the limits.
            config = {
                Dome.LlcName.AMCS.value: {"jmax": 1.0, "amax": 0.5, "vmax": 1.0},
                Dome.LlcName.LWSCS.value: {"jmax": 1.0, "amax": 0.5, "vmax": 1.0},
            }
            await self.csc.config_llcs(config)

            # The value of AMCS amax is too high.
            config = {
                Dome.LlcName.AMCS.value: {"jmax": 1.0, "amax": 1.0, "vmax": 1.0},
                Dome.LlcName.LWSCS.value: {"jmax": 1.0, "amax": 0.5, "vmax": 1.0},
            }
            try:
                await self.csc.config_llcs(config)
                self.fail("Expected a ValueError.")
            except ValueError:
                pass

            # The param AMCS smax doesn't exist.
            config = {
                Dome.LlcName.AMCS.value: {
                    "jmax": 1.0,
                    "amax": 0.5,
                    "vmax": 1.0,
                    "smax": 1.0,
                },
                Dome.LlcName.LWSCS.value: {"jmax": 1.0, "amax": 0.5, "vmax": 1.0},
            }
            try:
                await self.csc.config_llcs(config)
                self.fail("Expected a KeyError.")
            except KeyError:
                pass

            # No parameter can be missing.
            config = {
                Dome.LlcName.AMCS.value: {"jmax": 1.0, "amax": 0.5},
                Dome.LlcName.LWSCS.value: {"jmax": 1.0, "amax": 0.5, "vmax": 1.0},
            }
            try:
                await self.csc.config_llcs(config)
                self.fail("Expected a KeyError.")
            except KeyError:
                pass

    async def test_fans(self):
        raise unittest.SkipTest("Not implemented")

    async def test_inflate(self):
        raise unittest.SkipTest("Not implemented")

    async def test_status(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=None, simulation_mode=1,
        ):
            # It should be possible to always execute the status command but the connection with the lower
            # level components only gets made in DISABLED and ENABLED state so that's why the state gets
            # set to ENABLED here.
            await salobj.set_summary_state(
                remote=self.remote, state=salobj.State.ENABLED
            )
            await self.csc.status()

            amcs_status = self.csc.lower_level_status[Dome.LlcName.AMCS.value]
            self.assertEqual(
                amcs_status["status"], Dome.LlcStatus.STOPPED.value,
            )
            self.assertEqual(
                amcs_status["positionActual"], 0,
            )

            apscs_status = self.csc.lower_level_status[Dome.LlcName.APSCS.value]
            self.assertEqual(
                apscs_status["status"], Dome.LlcStatus.CLOSED.value,
            )
            self.assertEqual(
                apscs_status["positionActual"], 0,
            )

            lcs_status = self.csc.lower_level_status[Dome.LlcName.LCS.value]
            self.assertEqual(
                lcs_status["status"], [Dome.LlcStatus.CLOSED.value] * 34,
            )
            self.assertEqual(
                lcs_status["positionActual"], [0.0] * 34,
            )

            lwscs_status = self.csc.lower_level_status[Dome.LlcName.LWSCS.value]
            self.assertEqual(
                lwscs_status["status"], Dome.LlcStatus.STOPPED.value,
            )
            self.assertEqual(
                lwscs_status["positionActual"], 0,
            )

            moncs_status = self.csc.lower_level_status[Dome.LlcName.MONCS.value]
            self.assertEqual(
                moncs_status["status"], Dome.LlcStatus.DISABLED.value,
            )
            self.assertEqual(
                moncs_status["data"], [0.0] * 16,
            )

            thcs_status = self.csc.lower_level_status[Dome.LlcName.THCS.value]
            self.assertEqual(
                thcs_status["status"], Dome.LlcStatus.DISABLED.value,
            )
            self.assertEqual(
                thcs_status["data"], [0.0] * 16,
            )

    async def test_bin_script(self):
        await self.check_bin_script(name="Dome", index=None, exe_name="run_dome.py")
