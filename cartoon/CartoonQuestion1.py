import csv
import json
import random
import tkinter as tk
import sys
import subprocess
from tkinter import messagebox
from PIL import Image, ImageTk

class CharacterGuesser:
    def __init__(self, master):
        self.master = master
        self.master.title("Character Guesser")
        self.master.geometry("800x600")
        self.master.state("zoomed")  # Maximized window
        self.master.configure(bg="black")
        
        # Load dataset and translations
        self.characters = self.load_dataset("cartoon/cartoons.csv")
        self.translations = self.load_translations("cartoon/translations.json")
        
        self.columns = ["Gender", "Human", "Princess", "Superhero", "Chinese", "Japan", 
                        "Villian", "Special","Relation", "Property", "Black Skin", "Power","Studio","Similar"]
        self.asked_values = {col: set() for col in self.columns}  
        self.remaining_characters = self.characters.copy()
        self.first_columns = ["Gender", "Human", "Superhero"]
        
        self.load_background()
        self.create_widgets()
        self.ask_next_question()

    def load_dataset(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def load_translations(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            return json.load(file)
    def translate(self, text):
        return self.translations.get(text, text)
    
        
    def load_background(self):
        # Load and display background image
        self.bg_image = Image.open("cartoon/1963321.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        
    def create_widgets(self):
        # Main Container
        self.container = tk.Frame(self.master, bg="white", padx=30, pady=30, width=500,height=550)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.container.pack_propagate(False)  # Prevent the container from resizing to fit its contents

        
        # Character Image
        self.img = Image.open("cartoon/5157654-removebg-preview.png")
        self.img = self.img.resize((250, 250), Image.LANCZOS)
        self.img_photo = ImageTk.PhotoImage(self.img)
        self.image_label = tk.Label(self.container, image=self.img_photo, bg="white")
        self.image_label.pack()
        
        # Question Label
        self.question_label = tk.Label(self.container, text="", font=('Arial', 14), wraplength=400, bg="white")
        self.question_label.pack(pady=20)
        
        # Button Frame
        self.btn_frame = tk.Frame(self.container, bg="white")
        self.btn_frame.pack(pady=10)
        
        self.yes_btn = tk.Button(self.btn_frame, text="YES", font=("Arial", 14), bg="#28a745", fg="white", width=10, command=lambda: self.handle_answer(True))
        self.yes_btn.pack(side=tk.LEFT, padx=10)
        
        self.no_btn = tk.Button(self.btn_frame, text="NO", font=("Arial", 14), bg="#dc3545", fg="white", width=10, command=lambda: self.handle_answer(False))
        self.no_btn.pack(side=tk.RIGHT, padx=10)

        # Home Button
        self.home_button = tk.Button(
            self.container,
            text="Home",            
            font=("Arial", 14),
            bg="#007bff",
            fg="white",
            width=10,
            height=1,
            command=lambda: sys.exit()
        )
        self.home_button.pack(pady=10)
    
    def ask_next_question(self):
        if len(self.remaining_characters) == 1:
            self.show_result()
            return
        if not self.columns:
            self.show_result()
            return
        
        if self.first_columns:
            column = random.choice(self.first_columns)
            self.first_columns.remove(column)
        else:
            # Delay asking Special, Actor related questions until the final stage
            possible_columns = [col for col in self.columns if col not in ["Villian", "Special", "Relation", "Property"]]
            if not possible_columns:
                possible_columns = self.columns  # Fallback to all remaining columns
            column = random.choice(self.columns)
        
        unique_values = list(set(character[column] for character in self.remaining_characters
                                 if character[column].strip() and character[column] not in self.asked_values[column]))
        
        if not unique_values:
            self.columns.remove(column)
            self.ask_next_question()
            return
        
        value = random.choice(unique_values)
        self.current_column = column
        self.current_value = value
        
        # Get translated question
        question_template = self.translate("Is the character") 
        question = f"{question_template} {self.translate(column)} {self.translate(value)}"
        self.question_label.config(text=self.translate(question))
    
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
            character_row = self.remaining_characters[0]
            character = character_row['Name']
            self.open_prediction_page(character)
        else:
            message = "I couldn't guess the character. Maybe they're not in my dataset."
        
            messagebox.showinfo("Result", message)
            sys.exit()


    def open_prediction_page(self, character):
        # Close the current window
        self.master.destroy()

        # Run the second program and pass the predicted data
        subprocess.run(["python", "cartoon/CartoonAnswer1.py", character])

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterGuesser(root)
    root.mainloop()
