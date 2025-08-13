# Virtual Piano

This project provides a small Tkinter application that displays an
88‑key piano keyboard. When the optional [`pygame`](https://www.pygame.org/)
package (specifically ``pygame.midi``) is installed, key presses send MIDI
events to the system's default synthesizer, producing realistic piano
sounds that sustain while keys are held and stop on release.

If ``pygame`` is unavailable, the program falls back to synthesizing short
sine‑wave notes. Those are rendered using the optional
[`simpleaudio`](https://pypi.org/project/simpleaudio/) library for
polyphonic playback or the Windows‑only ``winsound`` module for
monophonic playback.

## Requirements

- Python 3
- (optional) `pygame` for MIDI piano sounds
- (optional) `simpleaudio` for synthesized polyphonic playback

## Running

```bash
python chord_player.py
```

Without any optional libraries, the app still launches but produces only a
single synthesized tone at a time. Installing ``pygame`` provides the best
experience with real piano sounds.

