import json
import pathlib
import re
import subprocess
import sys
import unittest

sys.path.append("..")
from tv_recording.config import Config  # noqa: E402

max_resolution = re.search(
    r"\s(\d+x\d+)\s", str(subprocess.check_output(["xrandr"]))
).group(1)


class TestConfig(unittest.TestCase):
    def test_load_default_config(self):
        config = Config()
        expected = {
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
        }
        self.assertEqual(config.config, expected)

    def test_load_custom_config(self):
        custom_config = {
            "input": {
                "format": "x11grab",
                "video_size": "1280x720",
                "framerate": 60,
                "video_device": ":1.0",
            },
            "output": {
                "video_codec": "libx265",
                "preset": "medium",
                "crf": 23,
                "loglevel": "info",
            },
        }
        with open("test_config.json", "w") as f:
            json.dump(custom_config, f)
        config = Config(config_file="test_config.json")
        self.assertEqual(config.config, custom_config)
        # Clean up
        pathlib.Path("test_config.json").unlink()

    def test_get_default_value(self):
        config = Config()
        self.assertEqual(config.get("input.format"), "x11grab")
        self.assertEqual(config.get("output.preset"), "ultrafast")

    def test_get_custom_value(self):
        custom_config = {
            "input": {
                "format": "x11grab",
                "video_size": "1280x720",
                "framerate": 60,
                "video_device": ":1.0",
            },
            "output": {
                "video_codec": "libx265",
                "preset": "medium",
                "crf": 23,
                "loglevel": "info",
            },
        }
        with open("test_config.json", "w") as f:
            json.dump(custom_config, f)
        config = Config(config_file="test_config.json")
        self.assertEqual(config.get("input.video_size"), "1280x720")
        self.assertEqual(config.get("output.crf"), 23)

    def test_ffmpeg_args(self):
        config = Config()
        expected = [
            "-f",
            "x11grab",
            "-video_size",
            max_resolution,
            "-framerate",
            "30",
            "-i",
            ":0.0",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "0",
            "-loglevel",
            "error",
        ]
        self.assertEqual(config.ffmpeg_args, expected)
