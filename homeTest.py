import tkinter as tk
from PIL import Image, ImageTk
import subprocess

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

# Heading
heading_label = tk.Label(container, text="Guess Who?", font=("Arial", 24, "bold"), bg="white")
heading_label.pack(pady=10)

# Canvas for Animation
canvas = tk.Canvas(container, bg="white", width=300, height=300, highlightthickness=0)
canvas.pack()

# Load and resize the image
img = Image.open("6365294-removebg-preview.png")
img = img.resize((300, 300), Image.LANCZOS)
img_photo = ImageTk.PhotoImage(img)

# Add the image to the canvas
image_canvas = canvas.create_image(150, 150, image=img_photo)

# Animation Variables
scale_factor = 1.0  # Initial scale factor
scale_direction = 1  # Direction of scaling (1 for growing, -1 for shrinking)
rotation_angle = 0  # Initial rotation angle

# Function to animate the image
def animate_image():
    global scale_factor, scale_direction, rotation_angle

    # Scale the image
    if scale_factor >= 1.2 or scale_factor <= 0.8:
        scale_direction *= -1  # Reverse the scaling direction
    scale_factor += 0.01 * scale_direction

    # Rotate the image
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0

    # Apply scaling and rotation
    scaled_img = img.resize((int(300 * scale_factor), int(300 * scale_factor)), Image.LANCZOS)
    rotated_img = scaled_img.rotate(rotation_angle, expand=True)
    img_photo_animated = ImageTk.PhotoImage(rotated_img)

    # Update the canvas image
    canvas.itemconfig(image_canvas, image=img_photo_animated)
    canvas.image = img_photo_animated  # Keep a reference to avoid garbage collection

    # Repeat the animation
    root.after(20, animate_image)

# Start the animation
animate_image()

# Function to run the question1.py program when "Singers" button is clicked
def open_singer():
    subprocess.run(["python", "singer/question1.py"])

def open_animal():
    subprocess.run(["python", "animal/animalQuestion1.py"])

# Buttons
button_frame = tk.Frame(container, bg="white")
button_frame.pack()

yes_button = tk.Button(button_frame, text="Animals", font=("Arial", 14), bg="#28a745", fg="white", width=10, height=1, command=open_animal)
yes_button.pack(side=tk.LEFT, padx=10)

no_button = tk.Button(button_frame, text="Singers", font=("Arial", 14), bg="#dc3545", fg="white", width=10, height=1, command=open_singer)
no_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()