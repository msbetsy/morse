"""This module is responsible for the language versions of the program"""
from data import languages_words


class LanguageManager:
    """This class allows you to change the language version of the program. The default version is English, available
    language versions: English, Polish, French, German.
    Example:
    from languages import LanguageManager
    language = LanguageManager('FRE')
    language.change_language('EN')
    """

    def __init__(self, new_language='EN'):
        self.new_language = new_language
        self.title = languages_words[new_language]["title"]
        self.your_text = languages_words[new_language]["your_text"]
        self.morse_message = languages_words[new_language]["morse_message"]
        self.load_file = languages_words[new_language]["load_file"]
        self.convert = languages_words[new_language]["convert"]
        self.translator = languages_words[new_language]["translator"]
        self.copy_text = languages_words[new_language]["copy_text"]
        self.save = languages_words[new_language]["save"]
        self.delete = languages_words[new_language]["delete"]
        self.frequency = languages_words[new_language]["frequency"]
        self.start = languages_words[new_language]["start"]
        self.stop = languages_words[new_language]["stop"]
        self.save_sound = languages_words[new_language]["save_sound"]
        self.save_in_direction = languages_words[new_language]["save_in_direction"]
        self.load_from_direction = languages_words[new_language]["load_from_direction"]
        self.translator = languages_words[new_language]["translator"]
        self.from_language = languages_words[new_language]["from_language"]
        self.to_language = languages_words[new_language]["to_language"]

    def change_language(self, new_language):
        """Change language version of program.

        :param new_language: Selected language of the language version of the program.
        :type new_language: str
        """
        for key, value in languages_words[new_language].items():
            setattr(self, key, value)
