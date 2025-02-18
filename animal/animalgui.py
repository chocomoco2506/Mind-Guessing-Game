import csv
import random
import json
import tkinter as tk
from tkinter import messagebox

class AnimalGuesser:
    def __init__(self, master):
        self.master = master
        self.master.title("Animal Guesser")

        # Load translations and dataset
        self.translations = self.load_translations("translations.json")
        self.animals = self.load_dataset("animals.csv")
        self.columns = ["class", "size", "color", "body covering", "legs", "tail", "habitat", "fly", "venomous", "diet", "pet", "social behaviour", "speed"]
        self.remaining_animals = self.animals.copy()
        self.asked_values = {col: set() for col in self.columns}  # Track asked values for each column
        self.first_columns = ["class", "size", "habitat"]

        # Setup UI
        self.create_widgets()
        self.ask_next_question()

    # Load translations from JSON file
    def load_translations(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return json.load(file)

    # Load dataset from CSV
    def load_dataset(self, filename):
        animals = []
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                animals.append(row)
        return animals

    # Translate text using the loaded translations
    def translate(self, text):
        return self.translations.get(text, text)

    # Create GUI widgets
    def create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.pack()

        # Question Label
        self.question_label = tk.Label(
            self.main_frame, 
            text="", 
            font=('Arial', 16), 
            wraplength=400
        )
        self.question_label.pack(pady=20)

        # Buttons Frame
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.pack(pady=10)

        self.yes_btn = tk.Button(
            self.btn_frame, 
            text=self.translate("Yes"), 
            command=lambda: self.handle_answer(True), 
            width=10, 
            bg='green', 
            fg='white'
        )
        self.yes_btn.pack(side=tk.LEFT, padx=10)

        self.no_btn = tk.Button(
            self.btn_frame, 
            text=self.translate("No"), 
            command=lambda: self.handle_answer(False), 
            width=10, 
            bg='red', 
            fg='white'
        )
        self.no_btn.pack(side=tk.LEFT, padx=10)

        # Restart Button
        self.restart_btn = tk.Button(
            self.main_frame, 
            text=self.translate("Restart"), 
            command=self.restart_game, 
            width=10, 
            bg='blue', 
            fg='white'
        )
        self.restart_btn.pack(pady=10)

    # Ask the next question
    def ask_next_question(self):
        if len(self.remaining_animals) == 1:
            self.show_result()
            return

        # If no more columns are available, end the game
        if not self.columns:
            self.show_result()
            return

        # First, ask about class, size, or habitat
        if self.first_columns:
            column = random.choice(self.first_columns)
            self.first_columns.remove(column)
        else:
            column = random.choice(self.columns)

        # Get unique values for the selected column (excluding already asked values)
        unique_values = list(set(animal[column] for animal in self.remaining_animals 
                                 if animal[column].strip() and animal[column] not in self.asked_values[column]))
        
        if not unique_values:
            self.columns.remove(column)
            self.ask_next_question()
            return

        # Randomly select a value to ask about
        value = random.choice(unique_values)
        self.current_column = column
        self.current_value = value

        # Update question label
        question_template = self.translate("Is the animal") 
        question = f"{question_template} {self.translate(column)} {self.translate(value)}"
        self.question_label.config(text=self.translate(question))

    # Handle user's answer
    def handle_answer(self, answer):
        if answer:
            self.remaining_animals = [a for a in self.remaining_animals if a[self.current_column] == self.current_value]
        else:
            self.remaining_animals = [a for a in self.remaining_animals if a[self.current_column] != self.current_value]

        # Add the asked value to the set of asked values for this column
        self.asked_values[self.current_column].add(self.current_value)

        # Ask the next question
        self.ask_next_question()

    # Show the result
    def show_result(self):
        if self.remaining_animals:
            animal = self.remaining_animals[0]
            animal_name = animal['animal name']
            translated_animal_name = self.translate(animal_name)
            message = self.translate("I guess the animal is") + f": {translated_animal_name}!\n"
            message += f"{self.translate('Class')}: {self.translate(animal['class'])}\n"
            message += f"{self.translate('Habitat')}: {self.translate(animal['habitat'])}\n"
            message += f"{self.translate('Diet')}: {self.translate(animal['diet'])}"
        else:
            message = self.translate("I couldn't guess the animal. Maybe it's not in my dataset.")

        messagebox.showinfo(self.translate("Result"), message)

    # Restart the game
    def restart_game(self):
        self.remaining_animals = self.animals.copy()
        self.asked_values = {col: set() for col in self.columns}
        self.first_columns = ["class", "size", "habitat"]
        self.columns = ["class", "size", "color", "body covering", "legs", "tail", "habitat", "fly", "venomous", "diet", "pet", "social behaviour", "speed"]
        self.ask_next_question()

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalGuesser(root)
    root.mainloop()