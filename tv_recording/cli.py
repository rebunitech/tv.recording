"""
A command line interface for tv_recording.
"""
import argparse
import datetime
import logging
import subprocess
from pathlib import Path

from .config import Config
from .db import Database


class CLI:
    """
    A command line interface for tv_recording.
    """

    def __init__(
        self, args: argparse.Namespace, logger: logging.Logger = None
    ):
        """
        Construct a CLI.
        """
        self.args = args
        self.logger = logger or logging.getLogger(__name__)
        self.config = Config(args.config, logger)
        self.db = Database(logger)

    def run(self):
        """
        Main entry point.
        """
        self.logger.info("tv_recording.cli.CLI.run()")
        current_time = datetime.datetime.now()
        path = Path(
            current_time.strftime("%Y-%m-%d_%H-%M-%S")
            + "_"
            + str(self.args.output)
        )
        command = [
            "ffmpeg",
            *self.config.ffmpeg_args,
            path.absolute().as_posix(),
        ]
        process = subprocess.Popen(command)

        logging.info("Recording to %s", path.absolute().as_posix())

        # Add recording to database
        self.db.add_recording(
            path.absolute().as_posix(),
            datetime.datetime.now().timestamp(),
        )

        try:
            # Wait for the process to finish
            process.communicate()
        except KeyboardInterrupt:
            # If the user presses Ctrl+C, kill the process
            process.kill()
            process.wait()

        # Set end time in database
        self.db.set_end_time(
            path.absolute().as_posix(),
            datetime.datetime.now().timestamp(),
        )
