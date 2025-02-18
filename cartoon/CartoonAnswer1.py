import sys
import tkinter as tk
from PIL import Image, ImageTk
import json  # Import the json module
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play the music (without looping)
pygame.mixer.music.load("cartoon/Answer.mp3")  # Replace with your file


# Keep the program running while the music plays
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)  # Prevents high CPU usage


# Get prediction from command-line arguments
predicted_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"

# Load Myanmar translations from JSON file
#with open("animal/translations.json", "r", encoding="utf-8") as file:
    #myanmar_translation = json.load(file)



# Extract first word of the predicted name
first_word = predicted_name.split()[0] if predicted_name != "Unknown" else predicted_name

# Determine image based on the first word
image_name = f"cartoon/Photo/{first_word}.jpg" if first_word != "Unknown" else "default.jpg"

# Initialize tkinter window
root = tk.Tk()
root.title("Prediction Page")
root.geometry("800x600")
root.state("zoomed")
root.configure(bg="black")

# Background Image
def update_bg(event=None):
    global bg_photo
    bg_image = Image.open("cartoon/1963321.jpg")
    bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label.config(image=bg_photo)

bg_image = Image.open("1963321.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

root.bind("<Configure>", update_bg)

# Main UI container
container = tk.Frame(root, bg="white", padx=30, pady=30, width=500, height=500)
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
container.pack_propagate(False)  # Prevent the container from resizing to fit its contents


# Title Label
title_label = tk.Label(container, text="သင်စဉ်းစားနေတဲ့ ကာတွန်းဇာတ်ကောင်က....", font=("Arial", 20, "bold"), bg="white",wraplength=400)
title_label.pack()

# Predicted Image
try:
    predicted_img = Image.open(image_name)
except FileNotFoundError:
    predicted_img = Image.open("default.jpg")  # Default image if not found
predicted_img = predicted_img.resize((200, 200), Image.LANCZOS)
predicted_photo = ImageTk.PhotoImage(predicted_img)

image_label = tk.Label(container, image=predicted_photo, bg="white")
image_label.pack()


name_label = tk.Label(container, text=f"{predicted_name}", font=("Arial", 18), bg="white")
name_label.pack(pady=10)


pygame.mixer.music.play()


# Restart Button
def restart_game():
    root.destroy()

restart_button = tk.Button(container, text="Home", font=("Arial", 14), bg="#007bff", fg="white", width=10, command=restart_game)
restart_button.pack(pady=20)

root.mainloop()