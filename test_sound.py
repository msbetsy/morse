"""This module contains unit tests for SoundManager class."""
import pytest

from sound import SoundManager


class TestSound:
    """This class contains tests for SoundManager class."""
    input_data_conversion = [
        (".", "88200"),
        ("-", "176400"),
        ("- .", "352800"),
        ("- / .", "529200"),
        ("- /", "441000"),
        (". /", "352800"),
        ("/", "308700")
    ]

    input_data_is_morse = [
        ('.'),
        ('u'),
        ('/')
    ]

    @pytest.mark.parametrize("text, output", input_data_conversion)
    def test_morse_to_sound(self, text, output):
        """This test checks if the message in Morse code will have have the correct length when it will be an audio
        Morse code.
        """
        object = SoundManager()
        length_array = str(len(object.morse_text_to_sound(text_to_sound=text)))
        assert length_array == output

    @pytest.mark.parametrize("text", input_data_is_morse)
    def test_is_morse(self, text):
        """This test checks if the message in Morse is in Morse code."""
        object = SoundManager()
        with pytest.raises(Exception):
            assert object.create_sound_array(text)
