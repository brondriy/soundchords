# Virtual Piano

This project provides a small Tkinter application that displays an
88‑key piano keyboard and synthesises short piano‑like tones for each key
using a mix of harmonics, an exponential decay envelope and a touch of
reverb for added realism. The optional
[`simpleaudio`](https://pypi.org/project/simpleaudio/) library enables
polyphonic playback, while the Windows‑only ``winsound`` module offers a
monophonic fallback. No external MIDI devices or additional dependencies
are required.

## Requirements

- Python 3
- (optional) `simpleaudio` for synthesized polyphonic playback

## Running

```bash
python chord_player.py
```

Without ``simpleaudio`` installed the app still launches but produces only
a single synthesized tone at a time using ``winsound``.

