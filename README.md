# Virtual Piano

This project provides a small Tkinter application that displays an
88‑key piano keyboard. Each key synthesizes a short sine wave with a
fade‑out so the note lingers briefly after it is clicked.

The program prefers the optional [`simpleaudio`](https://pypi.org/project/simpleaudio/)
package for playback, which allows multiple notes to overlap. If
`simpleaudio` is missing, it falls back to the Windows‑only `winsound`
module and can play only one note at a time.

## Requirements

- Python 3
- (optional) `simpleaudio` for polyphonic playback

## Running

```bash
python chord_player.py
```

On Windows without `simpleaudio`, the program still runs but is limited
to monophonic sound.

