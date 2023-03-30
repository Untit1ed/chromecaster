# Chromecaster

Chromecaster is a Python-based application that allows you to remotely control your local Chromecast device. With this app, you can easily send videos to your Chromecast and control its playback from your computer or smartphone, using either a Telegram bot or NTFY notifications.

## Installation

To use Chromecaster, you'll need to install Python 3.x


#### POSIX:

	python -m venv env
	source ./env/bin/activate
	pip install --upgrade pip
	pip install -e .

#### WINDOWS:

	python -m venv env
	.\env\Scripts\Activate.ps1
	pip install --upgrade pip
	pip install -e .
	
Then modify `.env` file with your chromcast device name and your telegram bot token. You'll need to create a bot and obtain a bot token from the BotFather.
	
## Usage
To use Chromecaster, simply run `main.py` script.

You can then send commands to your bot to control your Chromecast. 

The following commands are supported:

* `<video_url>` - plays the video if a URL was provided in the message
* `<timecode>` - if a timecode in the format of `HH:MM:SS` was provided, then the currently playing video will play at the specified timestamp
* `<float>` - if a float value between `0.5` and `2` was provided, then the current video will play at the provided rate
* `<0-100>` - if a value between `0` and `100` was provided, then the Chromecast volume will be adjusted accordingly
* `+<number>`, `-<number>` - if a number preceded with `+` or `-` was provided, then the video will fast forward or rewind by the provided amount of seconds

For example, to play a YouTube video on your Chromecast, you can send the following message to your Telegram bot:
```
Video Tile https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

To adjust the volume of your Chromecast, you can send a message like:

```
50
```

To fast forward the video by 30 seconds, you can send a message like:

```
+30
```

Note that timecodes, floats, and volume values must be sent as separate messages, and cannot be combined with other commands or text.
