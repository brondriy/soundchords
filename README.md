# Chord Player

This project provides a small Tkinter application that plays major chords
using only Python's standard library. Audio playback relies on the
`winsound` module, which is available on Windows.

## Requirements

- Python 3 on Windows

No third-party packages are needed. On non-Windows platforms the program runs
but remains silent because `winsound` is unavailable.

## Running

```bash
python chord_player.py
```

