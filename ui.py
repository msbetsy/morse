from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfile
from data import characters_in_morse
from languages import LanguageManager
from PIL import Image, ImageTk
from sound import SoundManager

BG_COLOUR = "#0F3057"
FG_COLOUR = "#008891"
BG_ENTRY_COLOUR = "#E7E7DE"
WIDTH_FLAG = 30
HEIGHT_FLAG = 20


class MorseInterface:
    def __init__(self):

        self.language = LanguageManager()
        self.sound = SoundManager()

        self.window = Tk()
        self.window.title("Fun with Morse")
        self.window.geometry("1000x700")
        self.window.config(padx=40, pady=20, bg=BG_COLOUR)
        self.language_to = StringVar(self.window)
        self.language_to.set("Choose option")
        options_list = ["To Morse", "From Morse"]
        self.options_menu = OptionMenu(self.window, self.language_to, *options_list)
        self.options_menu.config(width=16)
        self.options_menu.place(x=750, y=215)

        img_en = Image.open("./images/united_kingdom.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_pl = Image.open("./images/poland.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_fre = Image.open("./images/france.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        img_ger = Image.open("./images/germany.png").resize((WIDTH_FLAG, HEIGHT_FLAG))
        england_flag = ImageTk.PhotoImage(img_en)
        poland_flag = ImageTk.PhotoImage(img_pl)
        france_flag = ImageTk.PhotoImage(img_fre)
        germany_flag = ImageTk.PhotoImage(img_ger)

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
                                  justify='center', width=10, command=self.save_text_in_morse)
        self.save_button.place(x=750, y=410)

        self.delete_button = Button(self.window, text="Delete", font=('verdana', 15),
                                    justify='center', width=10, command=self.delete_text)
        self.delete_button.place(x=750, y=470)

        self.play_button = Button(self.window, text="play", font=('verdana', 15),
                                  justify='center', width=10, command=self.morse_text_to_sound)
        self.play_button.place(x=460, y=560)

        self.frequency_label = Label(self.window, text="Frequency", fg=BG_ENTRY_COLOUR,
                                     justify='left', bg=BG_COLOUR, font=('verdana', 12, 'bold'))
        self.frequency_label.place(x=110, y=530)

        self.frequency_scale = Scale(self.window, orient="horizontal", bg=FG_COLOUR, from_=400,
                                     to=900, resolution=50, sliderlength=20, length=150,
                                     fg=BG_ENTRY_COLOUR, font=('verdana', 10, 'bold'))
        self.frequency_scale.place(x=110, y=560)
        self.frequency_scale.set(self.sound.frequency)

        self.speed_label = Label(self.window, text="Speed", fg=BG_ENTRY_COLOUR,
                                 justify='left', bg=BG_COLOUR, font=('verdana', 12, 'bold'))
        self.speed_label.place(x=300, y=530)

        self.speed_scale = Scale(self.window, orient="horizontal", bg=FG_COLOUR, from_=0.5,
                                 to=2, resolution=0.5, sliderlength=20, length=100,
                                 fg=BG_ENTRY_COLOUR, font=('verdana', 10, 'bold'))
        self.speed_scale.set(1.0)
        self.speed_scale.place(x=300, y=560)

        self.stop_button = Button(self.window, text="stop", font=('verdana', 15),
                                  justify='center', width=10)
        self.stop_button.place(x=630, y=560)

        self.window.mainloop()

    def convert(self):
        self.output.delete("1.0", END)
        text = self.input_entry.get("1.0", END).lower()
        text = text.replace("\n", " ")
        if self.language_to.get() == "Choose option":
            messagebox.showwarning(title="Error", message="Choose language option")
        elif self.language_to.get() == "To Morse":
            self.convert_text_to_morse(text)
        elif self.language_to.get() == "From Morse":
            self.convert_morse_to_text(text)

    def convert_morse_to_text(self, text):
        self.converted_text = ""
        message = ""
        letter = ""
        many_options = False
        options = ""
        unknown_char = False
        unknown_char_list = []
        for char in text:
            possible_letters = "["
            count = 0
            if char != " ":
                letter += char
            elif char == "/":
                message += " "
            else:
                for key, value in characters_in_morse.items():
                    if letter == value:
                        possible_letters += key + ","
                        count += 1
                    else:
                        unknown_char = True
                        unknown_char_list.append(letter)
                if count == 1:
                    message += possible_letters[1:-1]
                elif count > 1:
                    message += possible_letters[:-1] + "]"
                    options += possible_letters[:-1] + "]"
                    many_options = True

                letter = ""
        unknown_char_list = list(set(unknown_char_list))
        if many_options:
            messagebox.showwarning(title="!", message="☛ " + str(options))
        if unknown_char:
            messagebox.showwarning(title="Error", message="Error ☛ " + str(unknown_char_list))
            self.output.insert(END, "ERROR " + str(unknown_char_list))
        else:
            self.output.insert(END, message)

    def convert_text_to_morse(self, text):
        unknown_char = False
        unknown_char_list = []
        self.text_in_morse = ""
        for character in text:
            try:
                self.text_in_morse += characters_in_morse[character] + " "
            except KeyError:
                unknown_char = True
                unknown_char_list.append(character)
        if unknown_char:
            unknown_char_list = list(set(unknown_char_list))
            messagebox.showwarning(title="Error", message="Error ☛ " + str(unknown_char_list))
            self.output.insert(END, "ERROR " + str(unknown_char_list))
        else:
            self.text_in_morse = self.text_in_morse[:-2]
            self.output.insert(END, self.text_in_morse)

    def delete_text(self):
        self.language_to.set('Choose option')
        self.output.delete("1.0", END)
        self.input_entry.delete("1.0", END)

    def copy_text_to_clipboard(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.text_in_morse)

    def save_text_in_morse(self):
        text = self.output.get("1.0", END)
        files = [('Text Document', '*.txt')]
        morse_file = asksaveasfile(title=self.language.save_in_direction, filetypes=files, defaultextension=files)
        if morse_file is not None:
            morse_file.write(text)
            morse_file.close()

    def load_file(self):
        files = [('Text Document', '*.txt')]
        text_file = askopenfile(mode='r', title=self.language.load_from_direction, filetypes=files,
                                defaultextension=files)
        if text_file is not None:
            text_inside = text_file.read()
            text_file.close()
        self.input_entry.insert("1.0", text_inside)

    def change_program_language(self):
        self.input_label.config(text=self.language.your_text)
        self.title_label.config(text=self.language.title)
        self.load_text_button.config(text=self.language.load_file)
        self.apply_button.config(text=self.language.convert)
        self.output_label.config(text=self.language.morse_message)
        self.copy_button.config(text=self.language.copy_text)
        self.save_button.config(text=self.language.save)

    def change_to_pl(self):
        self.language.chosen_language('PL')
        self.change_program_language()

    def change_to_en(self):
        self.language.chosen_language('EN')
        self.change_program_language()

    def change_to_fre(self):
        self.language.chosen_language('FRE')
        self.change_program_language()

    def change_to_ger(self):
        self.language.chosen_language('GER')
        self.change_program_language()

    def morse_text_to_sound(self):
        sound_speed = self.speed_scale.get()
        normal_speed = self.sound.duration
        self.sound.duration = int(self.sound.duration // sound_speed)
        freq = self.frequency_scale.get()
        self.sound.frequency = freq
        text = self.output.get("1.0", END)
        for char in text:
            if char == ".":
                self.sound.dot_sound()
                self.window.after(self.sound.space_between_morse_code)
            elif char == "-":
                self.sound.line_sound()
                self.window.after(self.sound.space_between_morse_code)
            elif char == " ":
                self.window.after(self.sound.space_between_chars - self.sound.space_between_morse_code)
            elif char == "/":
                self.window.after(self.sound.space_between_morse_code - 2 * (
                        self.sound.space_between_chars - self.sound.space_between_morse_code))
        self.sound.duration = normal_speed
