"""Tkinter piano with 88 keys.

The application synthesises short sine‑wave notes for each key and plays
them back using optional audio backends. ``simpleaudio`` provides
polyphonic playback when installed. On Windows systems the built-in
``winsound`` module offers a monophonic fallback. No external MIDI
devices or ``pygame`` dependency are required.
"""

from __future__ import annotations

import math
import struct
import wave
import tempfile
import tkinter as tk


# Try to import simpleaudio for polyphonic playback; fall back to winsound.
try:  # pragma: no cover - optional dependency
    import simpleaudio as sa
    _PLAY_WITH_SIMPLEAUDIO = True
except Exception:  # pragma: no cover - depends on environment
    sa = None
    _PLAY_WITH_SIMPLEAUDIO = False
    try:  # winsound is Windows-only
        import winsound
    except Exception:  # pragma: no cover - depends on environment
        winsound = None


SAMPLE_RATE = 44_100
DURATION = 1.2  # seconds for each note sample
DECAY = 0.3  # seconds to fade out

# Key geometry
WHITE_W = 20
WHITE_H = 150
BLACK_W = 12
BLACK_H = 90


def _build_note_list() -> list[str]:
    """Return names for all 88 piano keys from A0 to C8."""

    names = []
    sequence = [
        "A",
        "A#",
        "B",
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
    ]

    octave = 0
    for i in range(88):
        note = sequence[i % 12]
        if note == "C" and i != 0:
            octave += 1
        names.append(f"{note}{octave}")
    return names


NOTE_NAMES = _build_note_list()


def _build_freqs() -> dict[str, float]:
    """Map note names to their frequencies using equal temperament."""

    freqs = {}
    for idx, name in enumerate(NOTE_NAMES):
        semitone = idx - 48  # distance from A4
        freqs[name] = 440 * 2 ** (semitone / 12)
    return freqs


NOTE_FREQS = _build_freqs()


def synthesize(freq: float) -> bytes:
    """Return a PCM sample for a single note with a short decay."""

    total = int(SAMPLE_RATE * DURATION)
    decay_start = total - int(SAMPLE_RATE * DECAY)
    frames = []
    for i in range(total):
        sample = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        if i >= decay_start:
            sample *= (total - i) / (total - decay_start)
        frames.append(struct.pack("<h", int(sample * 32767)))
    return b"".join(frames)


def _prepare_audio() -> tuple[dict[str, "sa.WaveObject"], dict[str, str]]:
    """Precompute audio objects or temp files for all notes."""

    wave_objects: dict[str, "sa.WaveObject"] = {}
    file_paths: dict[str, str] = {}
    for name, freq in NOTE_FREQS.items():
        frames = synthesize(freq)
        if _PLAY_WITH_SIMPLEAUDIO:
            wave_objects[name] = sa.WaveObject(frames, 1, 2, SAMPLE_RATE)
        elif winsound is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                with wave.open(tmp, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(frames)
                file_paths[name] = tmp.name
    return wave_objects, file_paths


WAVE_OBJECTS, NOTE_FILES = _prepare_audio()


def play_note(name: str) -> None:
    """Play a note using the synthesized fallback."""

    if _PLAY_WITH_SIMPLEAUDIO:
        WAVE_OBJECTS[name].play()
    elif winsound is not None:  # pragma: no cover - Windows only
        winsound.PlaySound(
            NOTE_FILES[name],
            winsound.SND_FILENAME | winsound.SND_ASYNC,
        )
    else:  # pragma: no cover - no audio backend
        print("No audio backend available; cannot play sound")


def stop_note() -> None:
    """Stop playback for the synthesized fallback."""

    if winsound is not None:  # pragma: no cover - Windows only
        winsound.PlaySound(None, winsound.SND_PURGE)


def start_note(name: str) -> None:
    """Start playing a note."""

    play_note(name)


def end_note(name: str) -> None:
    """Stop a note started with :func:`start_note`."""

    stop_note()


def build_gui() -> tk.Tk:
    """Create the Tkinter interface resembling a piano."""

    root = tk.Tk()
    root.title("Virtual Piano")
    canvas = tk.Canvas(root, width=WHITE_W * 52, height=WHITE_H)
    canvas.pack()

    white_keys: list[tuple[int, str]] = []
    black_keys: list[tuple[int, str]] = []

    white_index = 0
    for name in NOTE_NAMES:
        if "#" in name:
            x = white_index * WHITE_W - BLACK_W // 2
            black_keys.append((x, name))
        else:
            x = white_index * WHITE_W
            white_keys.append((x, name))
            white_index += 1

    for x, name in white_keys:
        key = canvas.create_rectangle(
            x,
            0,
            x + WHITE_W,
            WHITE_H,
            fill="white",
            outline="black",
        )
        canvas.tag_bind(key, "<ButtonPress-1>", lambda _e, n=name: start_note(n))
        canvas.tag_bind(key, "<ButtonRelease-1>", lambda _e, n=name: end_note(n))
        canvas.tag_bind(key, "<Leave>", lambda _e, n=name: end_note(n))

    for x, name in black_keys:
        key = canvas.create_rectangle(
            x,
            0,
            x + BLACK_W,
            BLACK_H,
            fill="black",
            outline="black",
        )
        canvas.tag_bind(key, "<ButtonPress-1>", lambda _e, n=name: start_note(n))
        canvas.tag_bind(key, "<ButtonRelease-1>", lambda _e, n=name: end_note(n))
        canvas.tag_bind(key, "<Leave>", lambda _e, n=name: end_note(n))

    return root


def main() -> None:
    """Launch the piano GUI."""

    root = build_gui()
    root.mainloop()


if __name__ == "__main__":
    main()

