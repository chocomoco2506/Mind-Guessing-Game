import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("Prediction Page")
root.geometry("800x600")  # Set initial window size
root.state("zoomed")  # Maximized window with title bar
root.configure(bg="black")

# Function to update background image dynamically
def update_bg(event=None):
    global bg_photo
    bg_image = Image.open("flower.jpeg")
    bg_image = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label.config(image=bg_photo)

# Background Image Simulation
bg_image = Image.open("flower.jpeg")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Bind resize event to update_bg function
root.bind("<Configure>", update_bg)

# Main Container
container = tk.Frame(root, bg="white", padx=30, pady=30)
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title Label
title_label = tk.Label(container, text="You are thinking of...", font=("Arial", 20, "bold"), bg="white")
title_label.pack()

# Predicted Image
predicted_img = Image.open("6365294-removebg-preview.png")
predicted_img = predicted_img.resize((200, 200), Image.LANCZOS)
predicted_photo = ImageTk.PhotoImage(predicted_img)

image_label = tk.Label(container, image=predicted_photo, bg="white")
image_label.pack()

# Prediction Name
name_label = tk.Label(container, text="John Doe", font=("Arial", 18), bg="white")
name_label.pack(pady=10)

# Fact Section
fact_label = tk.Label(container, text="John Doe is a fictional name used to refer to an unknown person.John Doe is a fictional name used to refer to an unknown person. It is often used in legal contexts or as a placeholder name.",
                      font=("Arial", 14), bg="white", wraplength=400, justify="center")
fact_label.pack(pady=10)

# Restart Button
def restart_game():
    root.destroy()
    # You can replace this with code to open the home window

restart_button = tk.Button(container, text="Restart", font=("Arial", 14), bg="#007bff", fg="white", width=10, height=1, command=restart_game)
restart_button.pack(pady=20)

root.mainloop()
