"""
A command line interface for tv_recording.
"""
import argparse
import datetime
import logging
import subprocess
from pathlib import Path

import psutil

from .config import Config
from .db import Database


class CLI:
    """
    A command line interface for tv_recording.
    """

    def __init__(
        self, args: argparse.Namespace, parser, logger: logging.Logger = None
    ):
        """
        Construct a CLI.
        """
        self.args = args
        self.parser = parser
        self.logger = logger or logging.getLogger(__name__)
        self.db = Database(logger)

    def execute(self):
        """
        Execute the CLI.
        """
        self.logger.debug("tv_recording.cli.CLI.execute()")
        if self.args.command == "manage":
            self.manage()
        elif self.args.command == "run":
            self.run()

    def run(self):
        """
        Main entry point.
        """
        self.config = Config(self.args.config, self.logger)
        self.logger.debug("tv_recording.cli.CLI.run()")
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
            "2>&1 & echo $!",
        ]

        logging.debug("Command: %s", " ".join(command))
        # Create STDOUT pipe

        process = subprocess.Popen(
            ["/bin/sh", "-c", " ".join(command)], stdout=subprocess.PIPE
        )
        subprocess_pid = int(process.stdout.readline())

        logging.debug("Recording to %s", path.absolute().as_posix())
        logging.debug("Process ID: %s", subprocess_pid)
        logging.debug("Parent Process ID: %s", process.pid)

        self.db.add_recording(
            subprocess_pid,
            process.pid,
            path.absolute().as_posix(),
            datetime.datetime.now().timestamp(),
        )

    def manage(self):
        """
        Manage recordings.
        """
        self.logger.debug("tv_recording.cli.CLI.manage()")

        if self.args.show_active:
            self.list()
        elif self.args.stop:
            self.stop()
        else:
            self.parser.print_help()

    def list(self):
        """
        List recordings.
        """
        self.logger.debug("tv_recording.cli.CLI.list()")
        recordings = self.db.get_active_recordings()

        print("-" * 82)
        print(
            "ID".center(5),
            "PID".center(7),
            "Path".center(35),
            "Start Time".center(20),
            "Status".center(10),
        )
        print("-" * 82)
        if not recordings:
            print("No active recordings.".center(82))
        else:
            for recording in recordings:
                file_name = Path(recording["path"]).name
                print(
                    "",
                    str(recording["id"]).ljust(5),
                    str(recording["pid"]).ljust(7),
                    file_name.ljust(35),
                    datetime.datetime.fromtimestamp(recording["start_time"])
                    .strftime("%Y-%m-%d %H:%M:%S")
                    .ljust(20),
                    "Recording".ljust(10),
                )
        print("-" * 82)

    def get_video_duration(self, filename):
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-i",
                    filename,
                    "-show_entries",
                    "format=duration",
                    "-v",
                    "quiet",
                    "-of",
                    "csv=p=0",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            duration = float(result.stdout)
            return duration
        except subprocess.CalledProcessError as e:
            self.logger.info("Error getting video duration: %s", e)
            return None

    def _set_end_time(self, recording):
        """
        Set end time in database.
        """

        start_time = recording["start_time"]
        path = recording["path"]
        if not Path(path).exists():
            self.logger.info("File %s does not exist.", path)
            return

        file_length = self.get_video_duration(path)
        self.logger.debug("File length: %s", file_length)
        self.logger.debug("Start time: %s", start_time)
        self.logger.debug("End time: %s", start_time + file_length)

        self.db.set_end_time(
            path,
            start_time + file_length,
        )

    def stop(self):
        """
        Stop a recording.
        """
        self.logger.debug("tv_recording.cli.CLI.stop()")
        recording = self.db.get_by_id(self.args.stop)

        if recording is None:
            print(
                "Stop failed. Recording not found, may be it is already "
                "stopped."
            )
            return
        try:
            pid = recording["pid"]
            process = psutil.Process(pid)
            process.terminate()
            process.wait()
            print("Recording stopped.")
        except psutil.NoSuchProcess as e:
            print(e)
            print(
                "Stop failed. Recording not found, may be it is already "
                "stopped."
            )

        self._set_end_time(recording)
