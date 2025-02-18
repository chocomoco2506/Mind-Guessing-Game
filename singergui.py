import csv
import random
import tkinter as tk
from tkinter import messagebox

class SingerGuesser:
    def __init__(self, master):
        self.master = master
        self.master.title("Singer Guesser")
        
        # Initialize game
        self.characters = self.load_dataset("singers.csv")
        self.columns = ["Type", "Nationality", "Gender", "Award", "Age", 
                       "MusicGenre", "GroupName", "GroupPosition", "PopularSong", "Relationship"]
        self.asked_values = {col: set() for col in self.columns}  # Track asked values for each column
        self.remaining_characters = self.characters.copy()
        self.first_columns = ["Gender", "Type", "Nationality"]
        
        # Setup UI
        self.create_widgets()
        self.ask_next_question()

    def load_dataset(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))

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
            text="Yes", 
            command=lambda: self.handle_answer(True), 
            width=10, 
            bg='green', 
            fg='white'
        )
        self.yes_btn.pack(side=tk.LEFT, padx=10)

        self.no_btn = tk.Button(
            self.btn_frame, 
            text="No", 
            command=lambda: self.handle_answer(False), 
            width=10, 
            bg='red', 
            fg='white'
        )
        self.no_btn.pack(side=tk.LEFT, padx=10)

    def ask_next_question(self):
        if len(self.remaining_characters) == 1:
            self.show_result()
            return

        # First, ask about gender, type, or nationality
        if self.first_columns:
            column = random.choice(self.first_columns)
            self.first_columns.remove(column)
        else:
            column = random.choice(self.columns)

        # Skip GroupName and GroupPosition for Solo artists
        if column in ["GroupName", "GroupPosition"]:
            if all(character["Type"] == "Solo" for character in self.remaining_characters):
                self.columns.remove(column)
                self.ask_next_question()
                return

        # Skip Relationship for non-Myanmar characters
        if column == "Relationship":
            if not any(character["Nationality"] == "Myanmar" for character in self.remaining_characters):
                self.columns.remove(column)
                self.ask_next_question()
                return

        # Get unique values for the selected column (excluding already asked values)
        unique_values = list(set(character[column] for character in self.remaining_characters 
                                 if character[column].strip() and character[column] not in self.asked_values[column]))
        
        if not unique_values:
            self.columns.remove(column)
            self.ask_next_question()
            return

        # Randomly select a value to ask about
        value = random.choice(unique_values)
        self.current_column = column
        self.current_value = value

        # Update question label
        self.question_label.config(text=f"Is the singer {column} {value}?")

    def handle_answer(self, answer):
        if answer:
            self.remaining_characters = [c for c in self.remaining_characters if c[self.current_column] == self.current_value]
        else:
            self.remaining_characters = [c for c in self.remaining_characters if c[self.current_column] != self.current_value]

        # Add the asked value to the set of asked values for this column
        self.asked_values[self.current_column].add(self.current_value)

        # Ask the next question
        self.ask_next_question()

    def show_result(self):
        if self.remaining_characters:
            singer = self.remaining_characters[0]
            message = f"I guess the singer is: {singer['Name']}!\n"
            message += f"Award: {singer['Award']}\n"
            message += f"Popular Song: {singer['PopularSong']}"
        else:
            message = "I couldn't guess the singer. Maybe they're not in my dataset."

        messagebox.showinfo("Result", message)
        self.master.destroy()

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = SingerGuesser(root)
    root.mainloop()