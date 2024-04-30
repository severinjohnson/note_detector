import numpy as np
import sounddevice as sd
from scipy.fft import fft, fftfreq
def frequency_to_note(frequency):
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    A4 = 440
    C5 = 523.25  # Correct C5 frequency for more accurate reference

    # Calculate the number of half-steps away from C5
    n = round(12 * np.log2(frequency / C5))

    # Calculate the corresponding note and octave
    note_index = n % 12
    octave = 5 + (n // 12)  # Start from octave 5 since we're calculating from C5
    note = NOTE_NAMES[note_index] + str(octave)

    return note

def listen_and_analyze(duration=5, sample_rate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Recording finished. Analyzing...")
    yf = fft(recording[:, 0])
    xf = fftfreq(n=len(yf), d=1 / sample_rate)
    magnitudes = np.abs(yf)
    return xf, magnitudes

if __name__ == "__main__":
    frequencies, magnitudes = listen_and_analyze()
    filtered_freqs_mags = [(freq, mag) for freq, mag in zip(frequencies, magnitudes) if mag > 1e-5 and freq > 0]
    top_freqs_mags = sorted(filtered_freqs_mags, key=lambda x: x[1], reverse=True)[:10]
    for freq, mag in top_freqs_mags:
        note = frequency_to_note(freq)
        print(f"Frequency: {freq:.1f} Hz, Magnitude: {mag:.2f}, Note: {note}")

