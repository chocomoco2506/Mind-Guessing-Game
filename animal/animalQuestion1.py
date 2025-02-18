import csv
import random
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

class AnimalGuesser:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess Who? - Animal Guesser")
        self.master.geometry("800x600")  # Set initial window size
        self.master.state("zoomed")  # Maximized window with title bar
        self.master.configure(bg="black")

        # Load translations and dataset
        self.translations = self.load_translations("animal/translations.json")
        self.animals = self.load_dataset("animal/animals.csv")
        
        self.columns = ["class", "body covering", "legs", "tail", "habitat", "venomous", "diet","climb","afraid","farm","special","pet","buffalo"]
        self.remaining_animals = self.animals.copy()
        self.asked_values = {col: set() for col in self.columns}  # Track asked values for each column
        self.first_columns = ["class","habitat","legs"]

        # Background Image Simulation
        self.bg_image = Image.open("1963321.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind resize event to update_bg function
        self.master.bind("<Configure>", self.update_bg)

        # Main Container (Fixed size: 500x500)
        self.container = tk.Frame(self.master, bg="white", padx=30, pady=30, width=500, height=560)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.container.pack_propagate(False)  # Prevent the container from resizing to fit its contents

        # Image Container
        self.img = Image.open("5157654-removebg-preview.png")
        self.img = self.img.resize((300, 300), Image.LANCZOS)
        self.img_photo = ImageTk.PhotoImage(self.img)

        self.image_label = tk.Label(self.container, image=self.img_photo, bg="white")
        self.image_label.pack()

        # Question Label
        self.question_label = tk.Label(
            self.container, 
            text="", 
            font=("Arial", 14), 
            bg="white", 
            wraplength=400
        )
        self.question_label.pack(pady=20)

        # Buttons Frame
        self.button_frame = tk.Frame(self.container, bg="white")
        self.button_frame.pack()

        self.yes_button = tk.Button(
            self.button_frame, 
            text=self.translate("Yes"), 
            font=("Arial", 14), 
            bg="#28a745", 
            fg="white", 
            width=10, 
            height=1, 
            command=lambda: self.handle_answer(True)
        )
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.no_button = tk.Button(
            self.button_frame, 
            text=self.translate("No"), 
            font=("Arial", 14), 
            bg="#dc3545", 
            fg="white", 
            width=10, 
            height=1, 
            command=lambda: self.handle_answer(False)
        )
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

        # Start the game
        self.ask_next_question()

    # Function to update background image dynamically
    def update_bg(self, event=None):
        self.bg_image = Image.open("1963321.jpg")
        self.bg_image = self.bg_image.resize((self.master.winfo_width(), self.master.winfo_height()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label.config(image=self.bg_photo)

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
            # Delay asking Special, Actor related questions until the final stage
            possible_columns = [col for col in self.columns if col not in ["special"]]
            if not possible_columns:
                possible_columns = self.columns  # Fallback to all remaining columns
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
            
            # Check if only two values exist for this column
            unique_values = list(set(a[self.current_column] for a in self.remaining_animals))
            if len(unique_values) == 1:
                # If there's only one value left, we can remove this column
                if self.current_column in self.columns:
                    self.columns.remove(self.current_column)

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

            # Pass the predicted data to the second program
            self.open_prediction_page(animal)
        else:
            message = self.translate("I couldn't guess the animal. Maybe it's not in my dataset.")
            messagebox.showinfo(self.translate("Result"), message)
            sys.exit()

    # Open the prediction page with the predicted data
    def open_prediction_page(self, animal):
        # Close the current window
        self.master.destroy()

        # Run the second program and pass the predicted data
        subprocess.run(["python", "animal/animalAnswer1.py", animal['animal name'], animal['class'], animal['habitat'], animal['diet']])

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalGuesser(root)
    root.mainloop()