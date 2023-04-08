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
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="set logging level",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=pathlib.Path,
        help="set config file path",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        required=True,
        help="set data directory path",
    )

    return parser


def get_args(args: List[str] = None) -> argparse.Namespace:
    """
    Get arguments
    """
    parser = get_parser()
    return parser.parse_args(args=args)


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
