"""The module allows to handle Morse code translation via the graphical interface."""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfile

from PIL import Image, ImageTk

from data import languages_words
from languages import LanguageManager
from sound import SoundManager
from conversion import ConversionManager

BG_COLOUR = "#0F3057"
FG_COLOUR = "#008891"
BG_ENTRY_COLOUR = "#E7E7DE"
WIDTH_FLAG = 30  # width of the flag in the corner of application
HEIGHT_FLAG = 20  # height of the flag in the corner of application


class MorseInterface:
    """This class allows to handle the operations via graphical interface. Those operations can be such as: translation
     messages from and to Morse code and save the messages, it allows to listen, stop listening and save audio Morse
     file with different frequencies.
    """

    def __init__(self):
        """Constructor method."""
        self.language = LanguageManager()
        self.sound = SoundManager()
        self.window = Tk()
        self.conversion = ConversionManager()

        self.window.title("Fun with Morse")
        self.window.geometry("1000x700")
        self.window.resizable(False, False)
        self.window.config(padx=40, pady=20, bg=BG_COLOUR)
        self.window.iconbitmap('./images/morse_icon.ico')
        self.language_to = StringVar(self.window)
        self.language_to.set(self.language.translator)
        self.options_list = [self.language.to_language, self.language.from_language]
        self.options_menu = OptionMenu(self.window, self.language_to, *self.options_list)
        self.options_menu.config(width=16)
        self.options_menu.place(x=750, y=215)
        self.translated_text = None

        # Add flags.
        img_en = Image.open("./images/united_kingdom.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_pl = Image.open("./images/poland.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_fre = Image.open("./images/france.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_ger = Image.open("./images/germany.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        england_flag = ImageTk.PhotoImage(img_en)
        poland_flag = ImageTk.PhotoImage(img_pl)
        france_flag = ImageTk.PhotoImage(img_fre)
        germany_flag = ImageTk.PhotoImage(img_ger)

        # Add buttons.
        self.button_en = Button(self.window, image=england_flag, highlightthickness=0, command=self.change_to_en)
        self.button_en.place(x=780, y=0)

        self.button_pl = Button(self.window, image=poland_flag, highlightthickness=0, command=self.change_to_pl)
        self.button_pl.place(x=820, y=0)

        self.button_fre = Button(self.window, image=france_flag, highlightthickness=0, command=self.change_to_fre)
        self.button_fre.place(x=860, y=0)

        self.button_ger = Button(self.window, image=germany_flag, highlightthickness=0, command=self.change_to_ger)
        self.button_ger.place(x=900, y=0)

        self.title_label = Label(self.window, text=self.language.title, bg=BG_COLOUR, fg=FG_COLOUR,
                                 font=("verdana", 35, "bold"), pady=30)
        self.title_label.place(x=100, y=20)

        self.input_label = Label(self.window, text=self.language.your_text, fg=BG_ENTRY_COLOUR,
                                 justify='left', bg=BG_COLOUR, font=('verdana', 12, 'bold'))
        self.input_label.place(x=0, y=190)

        self.input_entry = Text(self.window, font=('verdana', 12), height=10, width=60, bg=BG_ENTRY_COLOUR,
                                cursor="pencil")
        self.input_entry.place(x=110, y=130)

        self.load_text_button = Button(self.window, text=self.language.load_file, font=('verdana', 15),
                                       justify='center', width=10, command=self.load_file)
        self.load_text_button.place(x=750, y=160)

        self.apply_button = Button(self.window, text=self.language.convert, font=('verdana', 15),
                                   justify='center', width=10, command=self.convert)
        self.apply_button.place(x=750, y=250)

        self.output_label = Label(self.window, text=self.language.morse_message, fg=BG_ENTRY_COLOUR,
                                  justify='left', bg=BG_COLOUR, font=('verdana', 12, 'bold'))
        self.output_label.place(x=0, y=390)

        self.output = Text(self.window, font=('verdana', 12), height=10, width=60, bg=BG_ENTRY_COLOUR)
        self.output.place(x=110, y=330)

        self.copy_button = Button(self.window, text=self.language.copy_text, font=('verdana', 15),
                                  justify='center', width=10, command=self.copy_text_to_clipboard)
        self.copy_button.place(x=750, y=350)

        self.save_button = Button(self.window, text=self.language.save, font=('verdana', 15),
                                  justify='center', width=10, command=self.save_text)
        self.save_button.place(x=750, y=410)

        self.delete_button = Button(self.window, text=self.language.delete, font=('verdana', 15),
                                    justify='center', width=10, command=self.delete_text)
        self.delete_button.place(x=750, y=470)

        self.play_button = Button(self.window, text=self.language.start, font=('verdana', 15),
                                  justify='center', width=10, command=self.play_morse_sound)

        self.frequency_label = Label(self.window, text=self.language.frequency, fg=BG_ENTRY_COLOUR,
                                     justify='left', bg=BG_COLOUR, font=('verdana', 12, 'bold'))

        self.frequency_scale = Scale(self.window, orient="horizontal", bg=FG_COLOUR, from_=400,
                                     to=900, resolution=50, sliderlength=20, length=150,
                                     fg=BG_ENTRY_COLOUR, font=('verdana', 10, 'bold'))

        self.frequency_scale.set(self.sound.frequency)

        self.stop_button = Button(self.window, text=self.language.stop, font=('verdana', 15),
                                  justify='center', width=10, command=self.stop_playing)

        self.save_sound_button = Button(self.window, text=self.language.save_sound, font=('verdana', 15),
                                        justify='center', width=20, command=self.save_morse_sound)

        self.window.mainloop()

    def convert(self):
        """This method is used to program the action of the button responsible for choosing the translation of the text
        from or to the Morse code.
        """
        self.output.delete("1.0", END)
        text = self.input_entry.get("1.0", END)
        text = text.replace("\n", " ")
        if self.language_to.get() in list(languages_words[item]["translator"] for item in list(languages_words.keys())):
            messagebox.showwarning(title="Error", message=self.language.translator)
        elif self.language_to.get() in list(
                languages_words[item]["to_language"] for item in list(languages_words.keys())):
            self.show_widgets()
            self.translated_text = self.conversion.convert_text_to_morse(text[:-1])
            self.output.insert(END, self.translated_text)
        elif self.language_to.get() in list(
                languages_words[item]["from_language"] for item in list(languages_words.keys())):
            self.hide_widgets()
            self.translated_text = self.conversion.convert_morse_to_text(text)
            self.output.insert(END, self.translated_text)

    def delete_text(self):
        """Delete your text and Morse code from fields when the delete_button is clicked."""
        self.hide_widgets()
        self.language_to.set(self.language.translator)
        self.output.delete("1.0", END)
        self.input_entry.delete("1.0", END)

    def copy_text_to_clipboard(self):
        """Copy converted text to clipboard when the copy_button is clicked."""
        self.window.clipboard_clear()
        self.window.clipboard_append(self.transalted_text)

    def save_text(self):
        """Save converted text to the computer when the save_button is clicked."""
        text = self.output.get("1.0", END)
        if text is not None:
            files = [('Text Document', '*.txt')]
            morse_file = asksaveasfile(title=self.language.save_in_direction, filetypes=files, defaultextension=files)

            if morse_file is not None:
                morse_file.write(text)
                morse_file.close()

    def load_file(self):
        """Load text for translation from the computer when the load_text_button is clicked."""
        files = [('Text Document', '*.txt')]
        text_file = askopenfile(mode='r', title=self.language.load_from_direction, filetypes=files,
                                defaultextension=files)
        if text_file is not None:
            text_inside = text_file.read()
            text_file.close()
            self.input_entry.insert("1.0", text_inside)

    def change_program_language(self):
        """Change text version of the application when one of the flag buttons is clicked."""
        self.input_label.config(text=self.language.your_text)
        self.title_label.config(text=self.language.title)
        self.load_text_button.config(text=self.language.load_file)
        self.apply_button.config(text=self.language.convert)
        self.output_label.config(text=self.language.morse_message)
        self.copy_button.config(text=self.language.copy_text)
        self.save_button.config(text=self.language.save)
        self.delete_button.config(text=self.language.delete)
        self.frequency_label.config(text=self.language.frequency)
        self.play_button.config(text=self.language.start)
        self.stop_button.config(text=self.language.stop)
        self.save_sound_button.config(text=self.language.save_sound)
        self.options_list = [self.language.to_language, self.language.from_language]
        self.language_to.set(self.language.translator)
        languages_menu = self.options_menu["menu"]
        languages_menu.delete(0, END)
        for string in self.options_list:
            languages_menu.add_command(
                label=string,
                command=lambda value=string: self.language_to.set(value))

    def change_to_pl(self):
        """Change text version of the application to Polish."""
        self.language.change_language('PL')
        self.change_program_language()

    def change_to_en(self):
        """Change text version of the application to English."""
        self.language.change_language('EN')
        self.change_program_language()

    def change_to_fre(self):
        """Change text version of the application to French."""
        self.language.change_language('FRE')
        self.change_program_language()

    def change_to_ger(self):
        """Change text version of the application to German."""
        self.language.change_language('GER')
        self.change_program_language()

    def play_morse_sound(self):
        """Play the audio Morse code when the play_button is clicked."""
        freq = self.frequency_scale.get()
        self.sound.frequency = freq
        text_to_sound = self.output.get("1.0", END)
        self.sound.convert(self.sound.morse_text_to_sound(text_to_sound))
        self.sound.play_audio()

    def save_morse_sound(self):
        """Save the audio Morse code to audio file to the computer when the save_sound_button is clicked."""
        files = [('Sound', '*.wav')]
        morse_file = asksaveasfile(title=self.language.save_sound, filetypes=files, defaultextension=files)
        if morse_file is not None:
            freq = self.frequency_scale.get()
            self.sound.frequency = freq
            text_to_sound = self.output.get("1.0", END)
            self.sound.convert(self.sound.morse_text_to_sound(text_to_sound))
            self.sound.save(morse_file.name)
            morse_file.close()

    def stop_playing(self):
        """Stop audio Morse code playback when the stop_button is clicked."""
        self.sound.playing_object.stop()

    def show_widgets(self):
        """Show widgets supporting audio Morse code."""
        self.play_button.place(x=300, y=560)
        self.frequency_label.place(x=110, y=530)
        self.frequency_scale.place(x=110, y=560)
        self.frequency_scale.set(self.sound.frequency)
        self.stop_button.place(x=460, y=560)
        self.save_sound_button.place(x=630, y=560)

    def hide_widgets(self):
        """Hide widgets supporting audio Morse code."""
        self.play_button.place_forget()
        self.frequency_label.place_forget()
        self.frequency_scale.place_forget()
        self.frequency_scale.place_forget()
        self.stop_button.place_forget()
        self.save_sound_button.place_forget()
