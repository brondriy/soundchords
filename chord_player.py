import numpy as np
import tkinter as tk

try:
    import simpleaudio as sa
except ModuleNotFoundError:  # pragma: no cover - depends on environment
    sa = None
    print(
        "simpleaudio not installed. Install it with 'pip install simpleaudio' "
        "or configure an alternative audio backend."
    )

# Sample rate and duration for generated tones
SAMPLE_RATE = 44100
DURATION = 0.8  # seconds

# Frequencies for notes in the 4th octave
NOTE_FREQS = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}

# Major triads using the 4th octave
CHORDS = {
    "C": ["C", "E", "G"],
    "D": ["D", "F", "A"],
    "E": ["E", "G", "B"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "A": ["A", "C", "E"],
    "B": ["B", "D", "F"],
}

def generate_tone(freq: float) -> np.ndarray:
    """Generate a sine wave for a given frequency."""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
    tone = np.sin(freq * 2 * np.pi * t)
    return tone

def play_chord(notes: list[str]) -> None:
    """Play a chord composed of the provided notes."""
    if sa is None:
        print(
            "Cannot play audio because simpleaudio is not installed. "
            "See README for installation instructions."
        )
        return

    waves = [generate_tone(NOTE_FREQS[note]) for note in notes]
    audio = sum(waves)
    audio *= 32767 / np.max(np.abs(audio))  # Normalize to 16-bit range
    audio = audio.astype(np.int16)

    play_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()

def make_button(root: tk.Tk, name: str, notes: list[str]) -> None:
    tk.Button(root, text=name, command=lambda: play_chord(notes), width=10).pack(padx=5, pady=5)

def main() -> None:
    root = tk.Tk()
    root.title("Chord Player")

    for name, notes in CHORDS.items():
        make_button(root, name, notes)

    root.mainloop()

if __name__ == "__main__":
    main()
