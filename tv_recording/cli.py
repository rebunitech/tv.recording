"""
A command line interface for tv_recording.
"""
import argparse
import logging


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

    def run(self):
        """
        Main entry point.
        """
        self.logger.info("tv_recording.cli.CLI.run()")
