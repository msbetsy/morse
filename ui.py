from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from data import characters_in_morse
from languages import LanguageManager
from PIL import Image, ImageTk

BG_COLOUR = "#0F3057"
FG_COLOUR = "#008891"
BG_ENTRY_COLOUR = "#E7E7DE"
WIDTH_FLAG = 30
HEIGHT_FLAG = 20


class MorseInterface:
    def __init__(self):

        self.language = LanguageManager()

        self.window = Tk()
        self.window.title("Fun with Morse")
        self.window.geometry("1000x700")
        self.window.config(padx=40, pady=20, bg=BG_COLOUR)

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
                                   justify='center', width=10, command=self.convert_text_to_morse)
        self.apply_button.place(x=750, y=220)

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

        self.window.mainloop()

    def convert_text_to_morse(self):
        self.output.delete("1.0", END)
        text = self.input_entry.get("1.0", END).lower()
        text = text.replace("\n", " ")
        self.text_in_morse = ""
        for character in text:
            self.text_in_morse += characters_in_morse[character] + " "
        self.text_in_morse = self.text_in_morse[:-2]
        self.output.insert(END, self.text_in_morse)

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
