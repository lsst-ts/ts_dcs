__all__ = ["DomeCsc"]

import asyncio
import logging
import pathlib
import yaml
from lsst.ts import salobj
from .mock_controller import MockDomeController
from lsst.ts.Dome import task_scheduler

logging.basicConfig(level=logging.INFO)

_LOCAL_HOST = "127.0.0.1"


class DomeCsc(salobj.ConfigurableCsc):
    """Upper level Commandable SAL Component to interface with the LSST Dome lower level components."""

    def __init__(
        self,
        config_dir=None,
        initial_state=salobj.State.STANDBY,
        simulation_mode=0,
        mock_port=None,
    ):
        schema_path = (
            pathlib.Path(__file__).resolve().parents[4].joinpath("schema", "Dome.yaml")
        )

        self.reader = None
        self.writer = None
        self.config = None

        self.log = logging.getLogger("DomeCsc")

        self.mock_ctrl = None  # mock controller, or None if not constructed
        self.mock_port = mock_port  # mock port, or None if not used
        super().__init__(
            name="Dome",
            index=0,
            schema_path=schema_path,
            config_dir=config_dir,
            initial_state=initial_state,
            simulation_mode=simulation_mode,
        )

        self.lower_level_status = None

        self.log.info("__init__")

    async def connect(self):
        """Connect to the dome controller's TCP/IP port.

        Start the mock controller, if simulating.
        """
        self.log.info("connect")
        self.log.info(self.config)
        self.log.info(f"self.simulation_mode = {self.simulation_mode}")
        if self.config is None:
            raise RuntimeError("Not yet configured")
        if self.connected:
            raise RuntimeError("Already connected")
        if self.simulation_mode == 1:
            await self.start_mock_ctrl()
            host = _LOCAL_HOST
        else:
            host = self.config.host
        if self.simulation_mode != 0:
            if self.mock_ctrl is None:
                raise RuntimeError("In simulation mode but no mock controller found.")
            port = self.mock_ctrl.port
        else:
            port = self.config.port
        connect_coro = asyncio.open_connection(host=host, port=port)
        self.reader, self.writer = await asyncio.wait_for(
            connect_coro, timeout=self.config.connection_timeout
        )

        # Start polling for the status of the lower level components periodically.
        # task_scheduler.run_status_loop = True
        await task_scheduler.schedule_task_periodically(1, self.status)

        self.log.info("connected")

    async def disconnect(self):
        """Disconnect from the TCP/IP controller, if connected, and stop the mock controller, if running."""
        self.log.debug("disconnect")

        # Stop polling for the status of the lower level components periodically.
        task_scheduler.run_status_loop = False

        writer = self.writer
        self.reader = None
        self.writer = None
        if writer:
            try:
                writer.write_eof()
                await asyncio.wait_for(writer.drain(), timeout=2)
            finally:
                writer.close()
        await self.stop_mock_ctrl()

    async def start_mock_ctrl(self):
        """Start the mock controller.

        The simulation mode must be 1.
        """
        self.log.info("start_mock_ctrl")
        try:
            assert self.simulation_mode == 1
            if self.mock_port is not None:
                port = self.mock_port
            else:
                port = self.config.port
            self.mock_ctrl = MockDomeController(port)
            await asyncio.wait_for(self.mock_ctrl.start(), timeout=2)
        except Exception as e:
            err_msg = "Could not start mock controller"
            self.log.exception(e)
            self.fault(code=3, report=f"{err_msg}: {e}")
            raise

    async def stop_mock_ctrl(self):
        """Stop the mock controller, if running."""
        self.log.info("stop_mock_ctrl")
        mock_ctrl = self.mock_ctrl
        self.mock_ctrl = None
        if mock_ctrl:
            await mock_ctrl.stop()

    async def handle_summary_state(self):
        """Override of the handle_summary_state function to connect or disconnect to the lower level components (or
        the mock_controller) when needed."""
        self.log.info("handle_summary_state")
        # TODO It should be possible to always connect and not just in DISABLED or ENABLED state.
        if self.disabled_or_enabled:
            if not self.connected:
                await self.connect()
        else:
            await self.disconnect()

    async def read(self):
        """Utility function to read a string from the reader and unmarshal it
        :return: A dictionary with objects representing the string read.
        """
        read_bytes = await asyncio.wait_for(self.reader.readuntil(b"\r\n"), timeout=1)
        data = yaml.safe_load(read_bytes.decode())
        return data

    async def write(self, cmd):
        """Write the string st appended with a newline character."""
        st = yaml.safe_dump(cmd, default_flow_style=None)
        self.writer.write(st.encode() + b"\r\n")
        self.log.info(st)
        await self.writer.drain()

    async def do_moveAz(self, _data):
        """Move AZ."""
        self.assert_enabled()
        cmd = {"moveAz": {"azimuth": _data.azimuth}}
        self.log.info(f"Moving Dome to azimuth {_data.azimuth}")
        await self.write(cmd)

    async def do_moveEl(self, _data):
        """Move El."""
        self.assert_enabled()
        cmd = {"moveEl": {"elevation": _data.elevation}}
        self.log.info(f"Moving LWS to elevation {_data.elevation}")
        await self.write(cmd)

    async def do_stopAz(self, _data):
        """Stop AZ."""
        self.assert_enabled()
        cmd = {"stopAz": {}}
        await self.write(cmd)

    async def do_stopEl(self, _data):
        """Stop El."""
        self.assert_enabled()
        cmd = {"stopEl": {}}
        await self.write(cmd)

    async def do_stop(self, _data):
        """Stop."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_crawlAz(self, _data):
        """Crawl AZ."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_crawlEl(self, _data):
        """Crawl El."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_setLouver(self, _data):
        """Set Louver."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_closeLouvers(self, _data):
        """Close Louvers."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_stopLouvers(self, _data):
        """Stop Louvers."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_openShutter(self, _data):
        """Open Shutter."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_closeShutter(self, _data):
        """Close Shutter."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_stopShutter(self, _data):
        """Stop Shutter."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_park(self, _data):
        """Park."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def do_setTemperature(self, _data):
        """Set Temperature."""
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def config(self, _data):
        """Config command not to be executed by SAL.

        This command will be used to send the values of one or more parameters to configure the lower level
        components.
        """
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def fans(self, _data):
        """Fans command not to be executed by SAL.

        This command will be used to switch on or off the fans in the dome.
        """
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def inflate(self, _data):
        """Inflate command not to be executed by SAL.

        This command will be used to inflate or deflate the inflatable seal.
        """
        self.assert_enabled()
        raise salobj.ExpectedError("Not implemented")

    async def status(self):
        """Status command not to be executed by SAL.

        This command will be used to request the full status of all lower level components.
        """
        cmd = {"status": {}}
        await self.write(cmd)
        self.lower_level_status = await self.read()

    async def close_tasks(self):
        """Disconnect from the TCP/IP controller, if connected, and stop
        the mock controller, if running."""
        await super().close_tasks()
        await self.disconnect()

    async def configure(self, config):
        self.config = config

    async def implement_simulation_mode(self, simulation_mode):
        if simulation_mode not in (0, 1):
            raise salobj.ExpectedError(
                f"Simulation_mode={simulation_mode} must be 0 or 1"
            )

    @property
    def connected(self):
        if None in (self.reader, self.writer):
            return False
        return True

    @staticmethod
    def get_config_pkg():
        return "ts_config_mttcs"

    @classmethod
    def add_arguments(cls, parser):
        super(DomeCsc, cls).add_arguments(parser)
        parser.add_argument(
            "-s", "--simulate", action="store_true", help="Run in simuation mode?"
        )

    @classmethod
    def add_kwargs_from_args(cls, args, kwargs):
        super(DomeCsc, cls).add_kwargs_from_args(args, kwargs)
        kwargs["simulation_mode"] = 1 if args.simulate else 0
