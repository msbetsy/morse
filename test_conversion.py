"""This module contains unit tests for ConversionManager class."""
import pytest

from conversion import ConversionManager


class TestDecode:
    """This class contains tests for ConversionManager class."""
    input_data_conversion = [
        ("help", ".... . .-.. .--."),
        ("street 8", "... - .-. . . - / ---.."),
        ("hello ", ".... . .-.. .-.. --- /")
    ]

    input_data_letter_case = [
        ("hELp", ".... . .-.. .--."),
        ("Street 8", "... - .-. . . - / ---.."),
        ("HELLO ", ".... . .-.. .-.. --- /")
    ]

    input_data_unknown_characters = [
        ("mn#", "ERROR ['#']"),
        ("POQ", "ERROR ['q']"),
        ("hello * ", "ERROR ['*']")

    ]

    @pytest.mark.parametrize("text, output", input_data_conversion)
    def test_conversion_decode(self, text, output):
        """This test checks if the message is translated correctly to Morse code - message contains only the characters
         from the Morse code.
         """
        object = ConversionManager()
        assert object.convert_text_to_morse(text) == output

    @pytest.mark.parametrize("text, output", input_data_letter_case)
    def test_letter_case(self, text, output):
        """This test checks if the message is translated correctly from Morse code - message contains letters with
        different letter case, but all of them after editing are in Morse code.
        """
        object = ConversionManager()
        assert object.convert_text_to_morse(text) == output

    @pytest.mark.parametrize("text, output", input_data_unknown_characters)
    def test_unknown_characters_decode(self, text, output):
        """This test checks if the message is translated correctly from Morse code - message contains characters which
        aren't in Morse code.
        """
        object = ConversionManager()
        assert object.convert_text_to_morse(text) == output


class TestEncode:
    input_data_conversion = [("... --- ...", "sos"),
                             (".... . .-.. .--.", "help"),
                             ("... - .-. . . - / ---..", "street 8"),
                             (".... . .-.. .-.. --- /", "hello ")
                             ]

    input_data_unknown_characters = [("@", "ERROR ['@']"),
                                     (".. -- + . /", "ERROR ['+', '\"']")
                                     ]

    @pytest.mark.parametrize("text, output", input_data_conversion)
    def test_conversion_encode(self, text, output):
        """This test checks if the message is translated correctly from Morse code - all the characters are in Morse
        code.
        """
        object = ConversionManager()
        assert object.convert_morse_to_text(text) == output

    @pytest.mark.parametrize("text, output", input_data_conversion)
    def test_unknown_characters_encode(self, text, output):
        """This test checks if the message is translated correctly from Morse code to text - some of the characters
        aren't in Morse code.
        """
        object = ConversionManager()
        assert object.convert_morse_to_text(text) == output
