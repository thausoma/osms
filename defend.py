import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd

SAMPLING_RATE = 44100

NOTE_TO_HERTZ = {
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
}

def make_sound(frequency_hz, duration_sec):
    time_seconds = np.arange(int(duration_sec * SAMPLING_RATE)) / SAMPLING_RATE
    return np.cos(2 * np.pi * frequency_hz * time_seconds)

CHORD_FOR_NOTE = {
    'D5': ('G4','B4','D5'), 'E5': ('G4','C5','E5'),
    'F5': ('A4','C5','F5'), 'G5': ('C5','E5','G5'),
}

def sing_track(track):
    sound_fragments = []
    for note_name, duration_sec in track:
        if note_name == 'R':
            sound_fragments.append(np.zeros(int(duration_sec * SAMPLING_RATE)))
        else:
            chord = sum(0.2 * make_sound(NOTE_TO_HERTZ[n], duration_sec)
                        for n in CHORD_FOR_NOTE[note_name])
            sound_fragments.append(chord)
    return np.concatenate(sound_fragments)

MELODY = [
    ('E5',0.25),('D5',0.25),('E5',0.45),('R',0.05),('E5',0.45),('R',0.05),('E5',0.45),('R',0.05),('E5',0.25),('R',0.05),('D5',0.25),('G5',1.0),
    ('R',0.5),
    ('D5',0.25),('D5',0.25),('E5',0.45),('R',0.05),('E5',0.45),('R',0.05),('E5',0.45),('R',0.05),('E5',0.25),('R',0.05),('D5',0.25),('G5',1.0),
    ('G5',0.25),('E5',0.25),('D5',0.25),('R',0.30),('D5',0.25),('E5',0.25),('F5',0.25),('R',0.25),('E5',0.25),('R',0.25),('D5',1.0),
    ('G5',0.25),('E5',0.25),('D5',0.25),('R',0.30),('D5',0.25),('E5',0.25),('F5',0.25),('R',0.25),('E5',0.25),('R',0.25),('D5',1.0),
]

audio = sing_track(MELODY)
sf.write('vivaldi_chords.wav', audio, SAMPLING_RATE)
sd.play(audio, SAMPLING_RATE); sd.wait()

Y = np.fft.rfft(audio)
freqs_full = np.fft.rfftfreq(len(audio), d=1/SAMPLING_RATE)

plt.figure(figsize=(14, 5))
plt.plot(freqs_full, np.abs(Y) / len(audio))
plt.xlim(0, 2000)
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()