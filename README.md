# Chord Player

This project provides a small Tkinter application that plays major chords using synthesized sine waves.

## Requirements

- Python 3
- [numpy](https://pypi.org/project/numpy/)
- [simpleaudio](https://pypi.org/project/simpleaudio/) (optional, required for sound output)

Install dependencies with:

```bash
pip install -r requirements.txt
```

If `simpleaudio` is missing or fails to install (for example, on Windows it may require the Microsoft Visual C++ Build Tools), the program will run but audio playback will be disabled. Follow the message shown at runtime to install `simpleaudio` or configure an alternative audio backend.

## Running

```bash
python chord_player.py
```
