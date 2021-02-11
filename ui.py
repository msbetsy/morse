from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from data import characters_in_morse

BG_COLOUR = "#0F3057"
FG_COLOUR = "#008891"
BG_ENTRY_COLOUR = "#E7E7DE"


class MorseInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Morse converter")
        self.window.geometry("1000x700")
        self.window.config(padx=40, pady=30, bg=BG_COLOUR)

        self.score_label = Label(text="Convert text to Morse Code", bg=BG_COLOUR, fg=FG_COLOUR,
                                 font=("verdana", 35, "bold"), pady=20)
        self.score_label.grid(column=0, row=0, columnspan=3)

        self.input_label = Label(text='Type your text: ', fg=BG_ENTRY_COLOUR,
                                 bg=BG_COLOUR, font=('verdana', 12))
        self.input_label.grid(column=0, row=1)

        self.input_entry = Text(font=('verdana', 12), height=5, width=50, bg=BG_ENTRY_COLOUR,
                                cursor="pencil")
        self.input_entry.grid(column=1, row=1)

        self.load_text_button = Button(text='Load file', font=('verdana', 15), command=self.load_file)
        self.load_text_button.place(x=735, y=100)

        self.apply_button = Button(text='Apply', font=('verdana', 15), command=self.convert_text_to_morse)
        self.apply_button.place(x=750, y=150)

        self.output_label = Label(text='Your message in Morse: ', fg=BG_ENTRY_COLOUR,
                                  bg=BG_COLOUR, font=('verdana', 12))
        self.output_label.grid(column=0, row=3)

        self.output = Text(font=('verdana', 12), width=50, bg=BG_ENTRY_COLOUR)
        self.output.grid(column=1, row=3)

        self.copy_button = Button(text='Copy', font=('verdana', 15), command=self.copy_text_to_clipboard)
        self.copy_button.place(x=750, y=300)

        self.save_button = Button(text='Save', font=('verdana', 15), command=self.save_text_in_morse)
        self.save_button.place(x=750, y=400)

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
        morse_file = asksaveasfile(title='Save file', filetypes=files, defaultextension=files)
        if morse_file is not None:
            morse_file.write(text)
            morse_file.close()

    def load_file(self):
        files = [('Text Document', '*.txt')]
        text_file = askopenfile(mode='r', title='Load text file', filetypes=files, defaultextension=files)
        if text_file is not None:
            text_inside = text_file.read()
            text_file.close()
        self.input_entry.insert("1.0", text_inside)
