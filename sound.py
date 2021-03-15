"""The module allows the conversion from Morse text into audio Morse code."""
from tkinter import messagebox
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
    sounds_connected = sound.concatenate_sound_arrays(sound_first, sound_second)
    sound.convert(sounds_connected)
    sound.play_audio()
    sound.playing_object.wait_done()
    sound.save("file.wav")
	"""

    def __init__(self):
        """Constructor method."""
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
        :raises Exception: Error in Morse code.
        :return: An array with duration of characters.
        :rtype: numpy.ndarray, float64
        """
        if character == ".":
            numpy_array = np.linspace(0, self.duration, self.duration * self.sampling_ratio,
                                      False)  # create numpy array with duration*sampling_ratio steps
            array_dot = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros(self.space_between_morse_code)
            array = self.concatenate_sound_arrays(array_dot, array_space)
            return array
        elif character == "-":
            numpy_array = np.linspace(0, self.duration * 3, self.duration * 3 * self.sampling_ratio,
                                      False)  # create numpy array with duration*sampling_ratio steps
            array_line = np.sin(self.frequency * numpy_array * 2 * np.pi)
            array_space = np.zeros(self.space_between_morse_code)
            array = self.concatenate_sound_arrays(array_line, array_space)
            return array
        elif character == " ":
            array = np.zeros((self.space_between_chars - self.space_between_morse_code))
            return array
        elif character == "/":
            array = np.zeros((self.space_between_words - self.space_between_morse_code - 2 * (
                    self.space_between_chars - self.space_between_morse_code)))
            return array
        else:
            messagebox.showwarning(title="Error", message="Error ☛ " + str(character))
            raise Exception("Error in Morse code")

    def concatenate_sound_arrays(self, sound1, sound2):
        """Concatenate two arrays of sounds together.

        :param sound1: An array with sounds duration.
        :type sound1: numpy.ndarray, float64
        :param sound2: An array with sounds duration.
        :type sound2: numpy.ndarray, float64
        :return: An concatenated array with duration of characters.
        :rtype: numpy.ndarray, float64
        """
        sounds = np.concatenate((sound1, sound2))
        return sounds

    def morse_text_to_sound(self, text_to_sound):
        """Convert Morse code to Morse audio code.

        :param text_to_sound: A message in Morse code.
        :type text_to_sound: str
        :return: An array with duration of characters.
        :rtype: numpy.ndarray, float64
        """
        text = text_to_sound.replace("\n", " ")
        text = text.rstrip()
        if len(text) == 1 and text == "/":
            sound_array = np.zeros(self.space_between_words)
        else:
            if text[-1] == "/":
                text += " "
            sound_array = self.create_sound_array(text[0])
            for char in text[1:]:
                array_for_character = self.create_sound_array(char)
                sound_array = self.concatenate_sound_arrays(sound_array, array_for_character)
        return sound_array

    def play_audio(self):
        """Play audio morse code.

        :return: An object to be played.
        :rtype: class 'simpleaudio.shiny.PlayObject'
        """
        self.playing_object = sa.play_buffer(self.audio, 1, 2, self.sampling_ratio)
        return self.playing_object

    def convert(self, array_with_sounds):
        """Convert sine wave to 16-bit data.

        :param array_with_sounds: An array with sine wave and silence between sounds.
        :type array_with_sounds: numpy.ndarray, float64
        :return: A converted array to 16-bit data.
        :rtype: numpy.ndarray, int16
        """
        if np.max(np.abs(array_with_sounds)) != 0:
            audio = array_with_sounds * (2 ** 15 - 1) / np.max(np.abs(array_with_sounds))
            self.audio = audio.astype(np.int16)
        else:
            self.audio = array_with_sounds.astype(np.int16)
        return self.audio

    def save(self, filename):
        """Save sound in computer.

        :param: A name of the file to be saved.
        :type: str
        """
        wavio.write(filename, self.audio, self.sampling_ratio, sampwidth=2)
