import winsound

FREQUENCY = 650
DURATION = 80
SPACE_BETWEEN_MORSE = DURATION
SPACE_BETWEEN_CHARS = DURATION * 3
SPACE_BETWEEN_WORDS = DURATION * 7


class SoundManager:
    def __init__(self):
        self.frequency = FREQUENCY
        self.duration = DURATION
        self.space_between_chars = SPACE_BETWEEN_CHARS
        self.space_between_words = SPACE_BETWEEN_WORDS
        self.space_between_morse_code = SPACE_BETWEEN_MORSE

    def dot_sound(self):
        winsound.Beep(self.frequency, self.duration)

    def line_sound(self):
        winsound.Beep(self.frequency, 3 * self.duration)
