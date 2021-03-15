"""This module allows conversion messages using Morse code."""
from tkinter import messagebox

from data import characters_in_morse


class ConversionManager:
    """This class can be used to encode and decode messages using Morse code."""

    def convert_text_to_morse(self, text):
        """Convert text to Morse code.

        :param text: Text to translation to Morse code.
        :type text: str
        :raises KeyError: Exception when character isn't in Morse code.
        :return: Translated text to Morse code.
        :rtype: str
        """
        unknown_char = False
        unknown_char_list = []
        text_in_morse = ""
        text = text.lower().replace("\n", " ")
        for character in text:
            try:
                text_in_morse += characters_in_morse[character] + " "
            except KeyError:
                unknown_char = True
                unknown_char_list.append(character)

        if unknown_char:
            unknown_char_list = list(set(unknown_char_list))
            messagebox.showwarning(title="Error", message="Error ☛ " + str(unknown_char_list))
            converted_text = " ".join(("ERROR", str(unknown_char_list)))
            return converted_text
        else:
            converted_text = text_in_morse[:-1]
            return converted_text

    def convert_morse_to_text(self, text):
        """Convert Morse code to text.

        :param text: Morse code to translate.
        :type text: str
        :return: Translated Morse code to text.
        :rtype: str
        """
        message = ""
        letter = ""
        many_options = False  # When there is one possibility for text translation from Morse code
        options = ""  # Possible characters during translation
        unknown_char = False  # True when there is a character not included in Morse code dictionary
        unknown_char_list = []  # List of not included characters in Morse code dictionary
        text = "".join((text, " "))

        for char in text:
            possible_letters = "["
            count = 0

            if char == "." or char == "-":
                letter += char
            elif char == "/":
                message += " "
            elif char == " ":

                if letter != "":
                    if letter in characters_in_morse.values():
                        for key, value in characters_in_morse.items():
                            if letter == value:
                                possible_letters += key + ","
                                count += 1
                    if count == 1:
                        message += possible_letters[1:-1]
                    elif count > 1:
                        message += possible_letters[:-1] + "]"
                        options += possible_letters[:-1] + "]"
                        many_options = True

                    letter = ""
            else:
                unknown_char = True
                unknown_char_list.append(char)

        unknown_char_list = list(set(unknown_char_list))

        if many_options:
            messagebox.showwarning(title="!", message="☛ " + str(options))

        if unknown_char:
            messagebox.showwarning(title="Error", message="Error ☛ " + str(unknown_char_list))
            converted_text = "ERROR " + str(unknown_char_list)
        else:
            converted_text = message

        return converted_text
