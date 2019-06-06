import time
import winsound
from threading import Thread

import math
import sounddevice
from numpy import linspace, sin, pi, int16


def name(n):
    labels = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#']
    return labels[n % len(labels)] + str(int((n + (9 + 4 * 12)) / 12))


def freq(n):
    return int(440 * (math.pow(2, 1 / 12) ** n))


def frequency(pitch):
    notes = {name(n): freq(n) for n in range(-42, 60)}
    return notes[pitch.lower()]


def note(freq, dur, amp=1.0, sample_rate=44100):
    t = linspace(0, dur, dur * sample_rate)
    data = sin(2 * pi * freq * t) * amp
    return data.astype(int16)


def play(freq, dur, channels=None):
    plays([freq], dur, channels)


def plays(freqs, dur, channels=None):
    rate = 44100
    amp = 10000 / len(freqs)
    tone = note(freqs[0], dur, amp=amp, sample_rate=rate)
    for freq in freqs[1:]:
        tone += note(freq, dur, amp=amp, sample_rate=rate)
    sounddevice.play(tone, samplerate=rate, mapping=channels)
    time.sleep(dur)


def play2(freq, dur):
    winsound.Beep(freq, dur * 1000)
    time.sleep(dur)


def play_thread(freq, dur, channels=None):
    thread = Thread(target=play, args=(freq, dur, channels))
    thread.start()
    return thread


def plays_thread(freqs, dur, channels=None):
    thread = Thread(target=plays, args=(freqs, dur, channels))
    thread.start()
    return thread


if __name__ == '__main__':
    play2(frequency('a4'), 3)
    play(frequency('a4'), 3)
    plays([frequency('g6'), frequency('a4'), frequency('c2')], 3)

    t1 = play_thread(frequency('a2'), 2, 1)
    t2 = play_thread(frequency('c6'), 2, 2)
    t1.join()
    t2.join()
