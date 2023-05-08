"""
Configuration file for tv_recording
"""

import json
import logging
import os
import pathlib
from typing import Any, Dict, List, Union

from Xlib import display

disp = os.environ.get("DISPLAY")
if disp is not None:
    d = display.Display(disp)
    s = d.screen()
    max_resolution = f"{s.width_in_pixels}x{s.height_in_pixels}"
else:
    max_resolution = "1280x720"


DEFAULT_CONFIG = {
    "input": {
        "format": "x11grab",
        "video_size": max_resolution,
        "framerate": 30,
        "video_device": ":0.0",
    },
    "output": {
        "video_codec": "libx264",
        "preset": "ultrafast",
        "crf": 0,
        "loglevel": "error",
    },
    "database": {
        "path": pathlib.Path("recording.db"),
    },
}


class Config:
    """
    Configuration file for tv_recording
    """

    def __init__(
        self,
        config_file: Union[str, pathlib.Path] = None,
        logger: logging.Logger = None,
    ):
        """
        Construct a Config.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """
        Load configuration file.
        """
        self.logger.debug("tv_recording.config.Config.load()")
        if self.config_file is not None:
            with open(self.config_file, "r") as file:
                self.config = json.load(file)
        else:
            self.config = DEFAULT_CONFIG

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        """
        self.logger.debug("tv_recording.config.Config.get()")
        if "." in key:
            keys = key.split(".")
            if keys[0] in self.config:
                if keys[1] in self.config[keys[0]]:
                    return self.config[keys[0]][keys[1]]
                else:
                    return default
        return self.config.get(key, default)

    @property
    def ffmpeg_args(self) -> List[str]:
        """
        Get configuration as ffmpeg arguments.
        """
        self.logger.debug("tv_recording.config.Config.get_as_ffmpeg_args()")
        relative_commands = {
            "format": "f",
            "video_device": "i",
            "video_codec": "c:v",
        }
        args = []
        config = {
            **DEFAULT_CONFIG["input"],
            **DEFAULT_CONFIG["output"],
            **self.config.get("input", {}),
            **self.config.get("output", {}),
        }
        for key, value in config.items():
            args.append(f"-{relative_commands.get(key, key)}")
            args.append(str(value))
        return args
