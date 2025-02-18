import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("Guess Who? - Second Page")
root.geometry("800x600")  # Set initial window size
root.state("zoomed")  # Maximized window with title bar
root.configure(bg="black")

# Function to update background image dynamically
def update_bg(event=None):
    global bg_photo
    bg_image = Image.open("1963321.jpg")
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

# Image Container
img = Image.open("5157654-removebg-preview.png")
img = img.resize((300, 300), Image.LANCZOS)
img_photo = ImageTk.PhotoImage(img)

image_label = tk.Label(container, image=img_photo, bg="white")
image_label.pack()

# Question Text
question_label = tk.Label(container, text="Is your character a real person?", font=("Arial", 16), bg="white")
question_label.pack(pady=20)

# Buttons
button_frame = tk.Frame(container, bg="white")
button_frame.pack()



yes_button = tk.Button(button_frame, text="YES", font=("Arial", 14), bg="#28a745", fg="white", width=10, height=1, )
yes_button.pack(side=tk.LEFT, padx=10)

no_button = tk.Button(button_frame, text="NO", font=("Arial", 14), bg="#dc3545", fg="white", width=10, height=1,)
no_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
