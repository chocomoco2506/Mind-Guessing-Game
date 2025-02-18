import tkinter as tk
from PIL import Image, ImageTk
import subprocess








# Initialize main window
root = tk.Tk()
root.title("Mind Guessing Game!")
root.geometry("800x600")  # Set initial window size
root.state("zoomed")  # Maximized window with title bar
root.configure(bg="black")

# Load the GIF
gif_path = "quest.gif"
gif = Image.open(gif_path)

# Resize frames dynamically to fit the full screen
frames = []
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

try:
    while True:
        frame = gif.copy().resize((win_width, win_height), Image.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
        gif.seek(len(frames))  # Move to next frame
except EOFError:
    pass  # No more frames

# Label to hold the background
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)  # Stretch to full window

# Function to animate the GIF
def animate(index=0):
    bg_label.config(image=frames[index])
    root.after(100, animate, (index + 1) % len(frames))  # Loop animation

# Start animation
animate()

# Main Container
container = tk.Frame(root, bg="white", width=500, height=600, padx=30, pady=30)
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
container.pack_propagate(False) 

# Heading
heading_label = tk.Label(container, text="Mind Guessing Game!", font=("Arial", 24, "bold"), bg="white")
heading_label.pack(pady=0)

# Canvas for Animation (Image Section)
image_frame = tk.Frame(container, bg="white")
image_frame.pack(pady=0) # Add padding to separate from buttons

canvas = tk.Canvas(image_frame, bg="white", width=400, height=400, highlightthickness=0)
canvas.pack()

# Load and resize the image
img = Image.open("bar.png")
img = img.resize((400, 400), Image.LANCZOS)
img_photo = ImageTk.PhotoImage(img)

# Add the image to the canvas
image_canvas = canvas.create_image(200, 200, image=img_photo)


# Function to run the question1.py program when "Singers" button is clicked
# Function to run the question1.py program when "Singers" button is clicked
def open_singer():
   
    subprocess.run(["python", "singer/question1.py"])

def open_animal():
   
    subprocess.run(["python", "animal/animalQuestion1.py"])

def open_cartoon():

    subprocess.run(["python","cartoon/cartoonQuestion1.py"])



# Buttons Section
button_frame = tk.Frame(container, bg="white")
button_frame.pack(pady=30)  # Add padding to separate from the image

yes_button = tk.Button(button_frame, text="Animals", font=("Arial", 14), bg="#28a745", fg="white", width=10, height=1, command=open_animal)
yes_button.pack(side=tk.LEFT, padx=10)


no_button = tk.Button(button_frame, text="Singers", font=("Arial", 14), bg="#dc3545", fg="white", width=10, height=1, command=open_singer)
no_button.pack(side=tk.RIGHT, padx=10)

no1_button = tk.Button(button_frame, text="Cartoons", font=("Arial", 14), bg="#1E90FF", fg="white", width=10, height=1,command=open_cartoon)
no1_button.pack(side=tk.RIGHT, padx=10)




# Run the application
root.mainloop()
