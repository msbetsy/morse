from data import languages_words


class LanguageManager:
    def __init__(self, new_language='EN'):
        self.new_language = new_language
        self.title = languages_words[new_language]["title"]
        self.your_text = languages_words[new_language]["your_text"]
        self.morse_message = languages_words[new_language]["morse_message"]
        self.load_file = languages_words[new_language]["load_file"]
        self.convert = languages_words[new_language]["convert"]
        self.copy_text = languages_words[new_language]["copy_text"]
        self.save = languages_words[new_language]["save"]
        self.save_in_direction = languages_words[new_language]["save_in_direction"]
        self.load_from_direction = languages_words[new_language]["load_from_direction"]

    def chosen_language(self, new_language):
        for key, value in languages_words[new_language].items():
            setattr(self, key, value)
