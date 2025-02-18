import csv
import random
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

class SingerGuesser:
    def __init__(self, master):
        self.master = master
        self.master.title("Singer Guesser")
        self.master.geometry("800x600")
        self.master.state("zoomed")
        self.master.configure(bg="black")

        # Load translations and dataset
        self.translations = self.load_translations("singer/translations.json")
        self.characters = self.load_dataset("singer/singers.csv")
        self.columns = ["Type", "Nationality", "Gender", "Award", "Age", 
                        "MusicGenre", "GroupName", "GroupPosition", "PopularSong","Collaboration","Special","Actor","Special American","Special Korean"]
        self.asked_values = {col: set() for col in self.columns}  
        self.remaining_characters = self.characters.copy()
        self.first_columns = ["Gender", "Type", "Nationality"]

        # Load background image
        self.bg_label = tk.Label(self.master)
        self.bg_label.place(relwidth=1, relheight=1)
        self.update_bg()
        self.master.bind("<Configure>", self.update_bg)

        # Setup UI
        self.create_widgets()
        self.ask_next_question()

    def update_bg(self, event=None):
        """ Updates background dynamically when window resizes """
        global bg_photo
        bg_image = Image.open("1963321.jpg")
        bg_image = bg_image.resize((self.master.winfo_width(), self.master.winfo_height()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label.config(image=bg_photo)

    def load_translations(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return json.load(file)

    def load_dataset(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def translate(self, text):
        return self.translations.get(text, text)

    def create_widgets(self):
        self.container = tk.Frame(self.master, bg="white", width=500, height=560, padx=30, pady=30)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.container.pack_propagate(False)  

        img = Image.open("5157654-removebg-preview.png").resize((300, 300), Image.LANCZOS)
        self.img_photo = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.container, image=self.img_photo, bg="white")
        self.image_label.pack()

        self.question_label = tk.Label(self.container, text="", font=("Arial", 14), bg="white", wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.button_frame = tk.Frame(self.container, bg="white")
        self.button_frame.pack()

        self.yes_button = tk.Button(self.button_frame, text=self.translate("YES"), font=("Arial", 14), bg="#28a745", 
                                    fg="white", width=10, command=lambda: self.handle_answer(True))
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.no_button = tk.Button(self.button_frame, text=self.translate("NO"), font=("Arial", 14), bg="#dc3545", 
                                   fg="white", width=10, command=lambda: self.handle_answer(False))
        self.no_button.pack(side=tk.RIGHT, padx=10)

        # Home Button
        self.home_button = tk.Button(
            self.container,
            text=self.translate("Home"),
            font=("Arial", 14),
            bg="#007bff",
            fg="white",
            width=10,
            height=1,
            command=lambda: sys.exit()
        )
        self.home_button.pack(pady=10)

    def ask_next_question(self):
        # Base case: If only one character remains, show the result
        if len(self.remaining_characters) == 1:
            self.show_result()
            return

        # Base case: If no more columns are available, show the result
        if not self.columns:
            self.show_result()
            return

        # First, prioritize Gender, Type, and Nationality
        if self.first_columns:
            column = random.choice(self.first_columns)
            self.first_columns.remove(column)
        else:
            # Delay asking Special, Actor related questions until the final stage
            possible_columns = [col for col in self.columns if col not in ["PopularSong", "Special", "Actor", "Special American", "Special Korean"]]
            if not possible_columns:
                possible_columns = self.columns  # Fallback to all remaining columns
            column = random.choice(possible_columns)

        

        # Remove columns dynamically based on conditions
        if column in ["GroupName", "GroupPosition"] and all(c["Type"] == "Solo" for c in self.remaining_characters):
            if column in self.columns:
                self.columns.remove(column)
            self.ask_next_question()
            return

        if column in ["Actor", "Special"] and not any(c["Nationality"] == "Myanmar" for c in self.remaining_characters):
            if column in self.columns:
                self.columns.remove(column)
            self.ask_next_question()
            return

        if column == "Special American" and not any(c["Nationality"] == "American" for c in self.remaining_characters):
            if column in self.columns:
                self.columns.remove(column)
            self.ask_next_question()
            return

        if column == "Special Korean" and not any(c["Nationality"] == "Korean" for c in self.remaining_characters):
            if column in self.columns:
                self.columns.remove(column)
            self.ask_next_question()
            return

        # Pick a value that hasn't been asked before
        unique_values = list(set(c[column] for c in self.remaining_characters if c[column].strip() and c[column] not in self.asked_values[column]))

        # If no unique values are left for this column, remove the column and ask the next question
        if not unique_values:
            if column in self.columns:
                self.columns.remove(column)
            self.ask_next_question()
            return

        # Ask the question
        self.current_column = column
        self.current_value = random.choice(unique_values)
        question = f"{self.translate('Is the singer')} {self.translate(column)} {self.translate(self.current_value)}?"
        self.question_label.config(text=question)



    def handle_answer(self, answer):
        if answer:
            self.remaining_characters = [c for c in self.remaining_characters if c[self.current_column] == self.current_value]
        else:
            self.remaining_characters = [c for c in self.remaining_characters if c[self.current_column] != self.current_value]
            
            # Check if only two values exist for this column
            unique_values = list(set(c[self.current_column] for c in self.remaining_characters))
            if len(unique_values) == 1:
                # If there's only one value left, we can remove this column
                if self.current_column in self.columns:
                    self.columns.remove(self.current_column)

        self.asked_values[self.current_column].add(self.current_value)
        self.ask_next_question()

        
    def show_result(self):
        if self.remaining_characters:
            singer_name = self.remaining_characters[0]['Name']
            translated_singer_name = self.translate(singer_name)
            #message = self.translate("I guess the singer is") + f": {translated_singer_name}!"
            self.open_prediction_page(singer_name)
        else:
            message = self.translate("I couldn't guess the singer. Maybe they're not in my dataset.")

            messagebox.showinfo(self.translate("Result"), message)
            sys.exit()


    def open_prediction_page(self, singer_name):
        # Close the current window
        self.master.destroy()

        # Run the second program and pass the predicted data
        subprocess.run(["python", "singer/answer1.py",singer_name])

if __name__ == "__main__":
    root = tk.Tk()
    app = SingerGuesser(root)
    root.mainloop()