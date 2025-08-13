"""Tkinter app to play basic major chords without external libraries.

This script synthesizes simple sine waves and plays them using the
``winsound`` module available on Windows. Hold a button to loop a chord and
release it to stop playback immediately.

If ``winsound`` is unavailable (e.g., on non-Windows platforms) the
program will display a message and remain silent.
"""

from __future__ import annotations

import io
import math
import struct
import wave
import tkinter as tk

try:  # winsound is only present on Windows
    import winsound
except ImportError:  # pragma: no cover - depends on platform
    winsound = None
    print("winsound module not available; audio playback disabled")


SAMPLE_RATE = 44_100
# Length of the sample used for looping; shorter keeps latency low
DURATION = 1.0  # seconds


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



def _build_wave(notes: tuple[str, ...]) -> bytes:
    """Return a full WAV byte stream for the given notes."""

    frames = synthesize_chord(notes)
    with io.BytesIO() as buffer:
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(frames)
        return buffer.getvalue()


# Precompute wave data for all chords so playback can start instantly
CHORD_WAVES = {name: _build_wave(notes) for name, notes in CHORDS.items()}


def start_chord(name: str) -> None:
    """Begin looping the specified chord until stopped."""

    if winsound is None:  # pragma: no cover - platform dependent
        print("Cannot play audio: winsound is not available")
        return

    winsound.PlaySound(
        CHORD_WAVES[name],
        winsound.SND_MEMORY | winsound.SND_LOOP | winsound.SND_ASYNC,
    )


def stop_chord(_event: tk.Event | None = None) -> None:
    """Stop any currently playing chord."""

    if winsound is not None:  # pragma: no cover - platform dependent
        winsound.PlaySound(None, winsound.SND_PURGE)


def main() -> None:
    """Launch the graphical interface."""

    root = tk.Tk()
    root.title("Chord Player")
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="Chord Player",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#1e1e1e",
    )
    title.pack(pady=(10, 5))

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(padx=10, pady=10)

    buttons = list(CHORDS.items())
    for idx, (name, notes) in enumerate(buttons):
        row, col = divmod(idx, 4)
        btn = tk.Button(
            frame,
            text=name,
            font=("Segoe UI", 14, "bold"),
            width=4,
            fg="white",
            bg="#3a7ca5",
            activebackground="#33698d",
            activeforeground="white",
            relief=tk.FLAT,
        )
        btn.grid(row=row, column=col, padx=5, pady=5)
        btn.bind("<ButtonPress-1>", lambda _e, n=name: start_chord(n))
        btn.bind("<ButtonRelease-1>", stop_chord)
        btn.bind("<Leave>", stop_chord)

    root.mainloop()


if __name__ == "__main__":
    main()

