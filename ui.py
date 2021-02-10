from tkinter import *
from data import characters_in_morse
BG_COLOUR= "#0F3057"
FG_COLOUR="#008891"
BG_ENTRY_COLOUR="#E7E7DE"

class MorseInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Morse converter")
        self.window.geometry("1000x700")
        self.window.config(padx=40, pady=30, bg=BG_COLOUR)

        #self.canvas = Canvas(width=700, height=950, bg="white")
        self.score_label = Label(text="Convert text to Morse Code", bg=BG_COLOUR, fg=FG_COLOUR,
                                 font=("verdana",35,"bold"),pady=20)
        self.score_label.grid(column=0, row=0, columnspan=3)

        self.input_label = Label(text='Type your text: ', fg=BG_ENTRY_COLOUR,
                                 bg=BG_COLOUR,font=('verdana', 12))
        self.input_label.grid(column=0, row=1)

        self.input_entry = Text(font=('verdana', 12), height = 5,width=50, bg=BG_ENTRY_COLOUR,
                                 cursor="pencil")
        self.input_entry.grid(column=1, row=1)

        self.text_to_morse_apply= Button(text='Apply', font=('verdana', 15), command =self.convert_text_to_morse)
        self.text_to_morse_apply.grid(column=2,row=1, padx=20)

        self.output_label=Label(text='Your message in Morse: ', fg=BG_ENTRY_COLOUR,
                                 bg=BG_COLOUR,font=('verdana', 12))
        self.output_label.grid(column=0, row=3)

        self.output = Text(font=('verdana', 12), width=50, bg=BG_ENTRY_COLOUR)
        self.output.grid(column=1, row=3)

        self.window.mainloop()

    def convert_text_to_morse(self):
        text = self.input_entry.get("1.0", "end").lower()
        text = text.replace("\n"," ")
        text_in_morse=""
        for character in text:
            text_in_morse += characters_in_morse[character] + " "
