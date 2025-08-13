"""Tkinter app to play basic major chords without external libraries.

This script synthesizes simple sine waves and plays them using the
``winsound`` module available on Windows. Each chord is triggered by a
button in the GUI.

If ``winsound`` is unavailable (e.g., on non-Windows platforms) the
program will display a message and remain silent.
"""

from __future__ import annotations

import math
import struct
import tempfile
import wave
import tkinter as tk

try:  # winsound is only present on Windows
    import winsound
except ImportError:  # pragma: no cover - depends on platform
    winsound = None
    print("winsound module not available; audio playback disabled")


SAMPLE_RATE = 44_100
DURATION = 1.5  # seconds


# Frequencies for notes in the 4th octave
NOTE_FREQS = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
}


# Major triads using the 4th octave
CHORDS: dict[str, tuple[str, str, str]] = {
    "C": ("C", "E", "G"),
    "D": ("D", "F#", "A"),
    "E": ("E", "G#", "B"),
    "F": ("F", "A", "C"),
    "G": ("G", "B", "D"),
    "A": ("A", "C#", "E"),
    "B": ("B", "D#", "F#"),
}


def synthesize_chord(notes: tuple[str, ...]) -> bytes:
    """Return raw audio data for the given notes."""

    frames = []
    for i in range(int(SAMPLE_RATE * DURATION)):
        sample = sum(
            math.sin(2 * math.pi * NOTE_FREQS[n] * i / SAMPLE_RATE)
            for n in notes
        )
        sample = int(sample / len(notes) * 32767)
        frames.append(struct.pack("<h", sample))

    return b"".join(frames)


def play_chord(notes: tuple[str, ...]) -> None:
    """Synthesize and play the given chord."""

    if winsound is None:  # pragma: no cover - platform dependent
        print("Cannot play audio: winsound is not available")
        return

    data = synthesize_chord(notes)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(data)
        winsound.PlaySound(tmp.name, winsound.SND_FILENAME)


def main() -> None:
    root = tk.Tk()
    root.title("Chord Player")

    for name, notes in CHORDS.items():
        tk.Button(
            root,
            text=name,
            width=5,
            command=lambda n=notes: play_chord(n),
        ).pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

