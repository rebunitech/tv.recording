"""
Arguments parser for tv_recording
"""

import argparse
import logging
import pathlib
from typing import List

from tv_recording import __version__


def get_parser() -> argparse.ArgumentParser:
    """
    Get arguments parser
    """
    parser = argparse.ArgumentParser(
        prog="tv-record",
        description="TV Station Media Recorder",
        epilog="",
    )

    subparse = parser.add_subparsers(dest="command", required=True)
    execusion_parse = subparse.add_parser("run")
    management_parse = subparse.add_parser("manage")

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show program's version number and exit",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="ERROR",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="set logging level",
    )
    execusion_parse.add_argument(
        "-c",
        "--config",
        type=pathlib.Path,
        help="set config file path",
    )

    execusion_parse.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        required=True,
        help="set data directory path",
    )
    management_parse.add_argument(
        "--show-active",
        action="store_true",
        help="show active recordings",
    )
    # argument to stop a recording
    management_parse.add_argument(
        "--stop",
        type=int,
        help="stop a recording",
    )
    # argument to set end time of all recording in database
    # if the recording is not active, but time is not set
    management_parse.add_argument(
        "--set-end-time",
        action="store_false",
        help="set end time of all recording in database",
    )

    return parser


def get_parser_and_args(args: List[str] = None) -> argparse.Namespace:
    """
    Get arguments
    """
    parser = get_parser()
    return (parser.parse_args(args=args), parser)


def get_logger(log_level: str) -> logging.Logger:
    """
    Get logger
    """
    import logging

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=getattr(logging, log_level),
    )
    return logging.getLogger(__name__)
