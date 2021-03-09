"""The module allows the conversion from Morse text into audio Morse code."""
import wavio
import numpy as np
import simpleaudio as sa

FREQUENCY = 600  # sine frequency in Hz, can be float
SAMPLING_RATIO = 44100  # sampling rate in Hz, must be integer
DURATION = 1  # duration of dot in seconds
SPACE_BETWEEN_MORSE = SAMPLING_RATIO  # inter-element gap between the dots and dashes in Morse Code
SPACE_BETWEEN_CHARS = SAMPLING_RATIO * 3  # gap between letters
SPACE_BETWEEN_WORDS = SAMPLING_RATIO * 7  # gap between words


class SoundManager:
    """This class can be used to produce the audio Morse code from Morse code. The audio Morse code can be also play or
    save as audio file.
		Example:
		from sound import SoundManager
		sound = SoundManager()
		sound_first = sound.create_sound_array(' ')
		sound_second = sound.create_sound_array('.')
		converted_sound_first = convert(sound_first)
		converted_sound_first.play()
		sounds_connected = concatenate_sound_arrays(sound_first, sound_second)
		converted_sounds_connected = convert(sounds_connected)
		converted_sounds_connected.play()
        converted_sounds_connected.save("sounds")
	"""

    def __init__(self):
        self.frequency = FREQUENCY
        self.duration = DURATION
        self.sampling_ratio = SAMPLING_RATIO
        self.space_between_chars = SPACE_BETWEEN_CHARS
        self.space_between_words = SPACE_BETWEEN_WORDS
        self.space_between_morse_code = SPACE_BETWEEN_MORSE
        self.audio = None
        self.playing_object = None

    def create_sound_array(self, character):
        """Generate a sine wave and an array with silence between characters.
        :param character: A character to be converted to sine wave or silence array.
        :type character: str
        :return array: An array with duration of charactes.
        :rtype array: numpy.ndarray, float64
        """
        if character == ".":
            numpy_array = np.linspace(0, self.duration, self.duration * self.sampling_ratio,
                                      False)  # create numpy array with duration*sampling_ratio steps, ranging between
            # 0 and duration
            array_dot = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros((self.space_between_morse_code))
            array = self.concatenate_sound_arrays(array_dot, array_space)
            return array
        elif character == "-":
            numpy_array = np.linspace(0, self.duration * 3, self.duration * 3 * self.sampling_ratio,
                                      False)  # create numpy array with duration*sampling_ratio steps, ranging between
            # 0 and duration
            array_line = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros((self.space_between_morse_code))
            array = self.concatenate_sound_arrays(array_line, array_space)
            return array
        elif character == " ":
            array = np.zeros((self.space_between_chars - self.space_between_morse_code))
            return array
        elif character == "/":
            array = np.zeros((self.space_between_words - self.space_between_morse_code - 2 * (
                    self.space_between_chars - self.space_between_morse_code)))
            return array

    def concatenate_sound_arrays(self, sound1, sound2):
        """Concatenate two arrays of sounds together.
        :param sound1: An array with sounds duration.
        :type sound1: numpy.ndarray, float64
        :param sound2: An array with sounds duration.
        :type sound2: numpy.ndarray, float64
        :return sounds: An concatenated array with duration of charactes.
        :rtype sounds: numpy.ndarray, float64
        """
        sounds = np.concatenate((sound1, sound2))
        return sounds

    def play(self):
        """Play audio morse code."""
        self.playing_object = sa.play_buffer(self.audio, 1, 2, self.sampling_ratio)

    def convert(self, array_with_sounds):
        """Convert sine wave to 16-bit data.
        :param array_with_sounds: An array with sine wave and silence between sounds.
        :type array_with_sounds: numpy.ndarray, float64
        :return self.audio: A converted array to 16-bit data.
        :rtype self.audio: numpy.ndarray, int16
        """
        audio = array_with_sounds * (2 ** 15 - 1) / np.max(np.abs(array_with_sounds))
        self.audio = audio.astype(np.int16)
        return self.audio

    def save(self, filename):
        """Save sound in computer.
        :param filename: A name of the file to be saved.
        :type filename: str
        """
        wavio.write(filename, self.audio, self.sampling_ratio, sampwidth=2)
