import numpy as np
import wavio
import simpleaudio as sa

FREQUENCY = 600
SAMPLING_RATIO = 44100
DURATION = 1
SPACE_BETWEEN_MORSE = SAMPLING_RATIO
SPACE_BETWEEN_CHARS = SAMPLING_RATIO * 3
SPACE_BETWEEN_WORDS = SAMPLING_RATIO * 7


class SoundManager:
    def __init__(self):
        self.frequency = FREQUENCY
        self.duration = DURATION
        self.sampling_ratio = SAMPLING_RATIO
        self.space_between_chars = SPACE_BETWEEN_CHARS
        self.space_between_words = SPACE_BETWEEN_WORDS
        self.space_between_morse_code = SPACE_BETWEEN_MORSE
        self.audio = None
        self.playing_object = None

    def sound_array(self, character):
        if character == ".":
            numpy_array = np.linspace(0, self.duration, self.duration * self.sampling_ratio, False)
            array_dot = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros((self.space_between_morse_code))
            array = self.concatenate_sounds(array_dot, array_space)
            return array
        elif character == "-":
            numpy_array = np.linspace(0, self.duration * 3, self.duration * 3 * self.sampling_ratio, False)
            array_line = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros((self.space_between_morse_code))
            array = self.concatenate_sounds(array_line, array_space)
            return array
        elif character == " ":
            array = np.zeros((self.space_between_chars - self.space_between_morse_code))
            return array
        elif character == "/":
            array = np.zeros((self.space_between_words - self.space_between_morse_code - 2 * (
                    self.space_between_chars - self.space_between_morse_code)))
            return array

    def concatenate_sounds(self, sound1, sound2):
        sounds = np.concatenate((sound1, sound2))
        return sounds

    def play(self):
        self.playing_object = sa.play_buffer(self.audio, 1, 2, self.sampling_ratio)

    def convert(self, array_with_sounds):
        audio = array_with_sounds * (2 ** 15 - 1) / np.max(np.abs(array_with_sounds))
        self.audio = audio.astype(np.int16)
        return self.audio

    def save(self, filename):
        wavio.write(filename, self.audio, self.sampling_ratio, sampwidth=2)
