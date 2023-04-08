import argparse
import logging
import pathlib
import sys
import unittest
from unittest import mock

sys.path.append("..")

from tv_recording.parser import get_args, get_logger, get_parser  # noqa: E402


class TestArgsParser(unittest.TestCase):
    def test_get_args(self):
        test_args = [
            "-c",
            "test_config.json",
            "-o",
            "test_data_folder",
            "-l",
            "DEBUG",
        ]
        expected_parsed_args = argparse.Namespace(
            config=pathlib.Path("test_config.json"),
            output=pathlib.Path("test_data_folder"),
            log_level="DEBUG",
            version=False,
        )

        parsed_args = get_args(args=test_args)
        self.assertEqual(parsed_args.config, expected_parsed_args.config)
        self.assertEqual(parsed_args.output, expected_parsed_args.output)
        self.assertEqual(parsed_args.log_level, expected_parsed_args.log_level)

    def test_get_parser(self):
        parser = get_parser()
        parsed_args = parser.parse_args(
            ["-c", "test_config.json", "-o", "test_data_folder", "-l", "DEBUG"]
        )
        expected_parsed_args = argparse.Namespace(
            config=pathlib.Path("test_config.json"),
            output=pathlib.Path("test_data_folder"),
            log_level="DEBUG",
            version=False,
        )

        self.assertEqual(parsed_args.config, expected_parsed_args.config)
        self.assertEqual(parsed_args.output, expected_parsed_args.output)
        self.assertEqual(parsed_args.log_level, expected_parsed_args.log_level)

    @mock.patch("logging.getLogger")
    def test_get_logger(self, mock_logger):
        expected_logger = logging.getLogger(__name__)
        mock_logger.return_value = expected_logger

        self.assertEqual(get_logger(log_level="DEBUG"), expected_logger)
