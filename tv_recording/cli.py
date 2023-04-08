"""
A command line interface for tv_recording.
"""
import argparse
import logging
import subprocess
from pathlib import Path

from .config import Config


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

    def run(self):
        """
        Main entry point.
        """
        self.logger.info("tv_recording.cli.CLI.run()")
        path = Path(self.args.output)
        command = [
            "ffmpeg",
            *self.config.ffmpeg_args,
            path.absolute().as_posix(),
        ]
        process = subprocess.Popen(command)

        logging.info("Recording to %s", path.absolute().as_posix())
        # Wait for the process to finish
        process.communicate()
