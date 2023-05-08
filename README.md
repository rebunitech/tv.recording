# TV Station Media Recorder

Pure Python script to record TV stations from screen capture

## Requirements

* Python 3.8+
* [ffmpeg](https://ffmpeg.org/)
* [ffprobe](https://ffmpeg.org/ffprobe.html)

## Development

```bash
git clone git@github.com:rebunitech/tv.recording.git
cd tv.recording
pip install -r requirements.txt
pip install -e .
```
## Usage

```bash
usage: tv-record [-h] [-V] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] {run,manage} ...

TV Station Media Recorder

positional arguments:
  {run,manage}

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        set logging level


usage: tv-record run [-h] [-c CONFIG] -o OUTPUT

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        set config file path
  -o OUTPUT, --output OUTPUT
                        set data directory path


usage: tv-record manage [-h] [--show-active] [--stop STOP] [--set-end-time]

options:
  -h, --help      show this help message and exit
  --show-active   show active recordings
  --stop STOP     stop a recording
  --set-end-time  set end time of all recording in database
```


## License

[Apache License 2.0](LICENSE)

## Author

[Wendirad Demelash](http://github.com/wendirad)
