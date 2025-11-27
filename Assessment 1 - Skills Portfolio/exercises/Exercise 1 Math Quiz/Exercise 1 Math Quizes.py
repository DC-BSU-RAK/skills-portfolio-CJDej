import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from PIL import Image, ImageTk 

# --- PATH FINDER ---
# This ensures Python finds your images no matter where you run this script
base_folder = os.path.dirname(os.path.abspath(__file__))

HAPPY_IMG_PATH = os.path.join(base_folder, "Barney.jpg")
SCARY_IMG_PATH = os.path.join(base_folder, "Angry Trex.jpg")
RULER_IMG_PATH = os.path.join(base_folder, "Ruler.jpg")

# --- Configuration ---
BARNEY_PURPLE = "#8E44AD"
BARNEY_GREEN = "#2ECC71"
ERROR_RED = "#7B0000"
TEXT_COLOR = "#FFFFFF"

# --- Helper Function for Images ---
def load_and_resize_image(filepath, width, height):
    try:
        if not os.path.exists(filepath):
            print(f"Warning: Could not find {filepath}")
            return None
        img = Image.open(filepath)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# --- Functions ---

def displayMenu():
    clear_window()
    root.configure(bg=BARNEY_PURPLE)
    
    tk.Label(root, text="Barney's Edu-Tainment!", font=("Comic Sans MS", 24, "bold"), 
             bg=BARNEY_PURPLE, fg=BARNEY_GREEN).pack(pady=10)
    
    # Happy Image
    photo = load_and_resize_image(HAPPY_IMG_PATH, 200, 240)
    if photo:
        lbl = tk.Label(root, image=photo, bg=BARNEY_PURPLE)
        lbl.image = photo 
        lbl.pack(pady=5)

    tk.Label(root, text="Select Difficulty:", font=("Comic Sans MS", 14), 
             bg=BARNEY_PURPLE, fg="white").pack(pady=5)
    
    create_button("Easy Peasy", lambda: start_quiz("easy"))
    create_button("Middle School", lambda: start_quiz("moderate"))
    create_button("Big Brain", lambda: start_quiz("advanced"))
    
    create_button("Exit", root.quit, bg_color="tomato")


def create_button(text, command, bg_color=BARNEY_GREEN):
    tk.Button(root, text=text, font=("Comic Sans MS", 12), width=20, 
              bg=bg_color, fg="black", activebackground="yellow",
              command=command).pack(pady=4)


def randomInt(level):
    if level == "easy": return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate": return random.randint(10, 99), random.randint(10, 99)
    elif level == "advanced": return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-", "*", "/"])


def displayProblem():
    global current_question, num1, num2, operation, answer_entry, image_label

    clear_window()
    root.configure(bg=BARNEY_PURPLE) 

    tk.Label(root, text=f"Problem {current_question}/10", font=("Comic Sans MS", 14, "bold"), 
             bg=BARNEY_PURPLE, fg="yellow").pack(pady=5)
    
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    if operation == "/":
        num2 = random.randint(1, 9) if difficulty == "easy" else random.randint(2, 12)
        num1 = num2 * random.randint(1, 9) if difficulty == "easy" else num2 * random.randint(2, 12)

    op_symbol = {"*": "×", "/": "÷"}.get(operation, operation)

    # --- BARNEY ---
    photo = load_and_resize_image(HAPPY_IMG_PATH, 180, 220)
    image_label = tk.Label(root, image=photo, bg=BARNEY_PURPLE)
    image_label.image = photo
    image_label.pack(pady=2)
    
    # We display the math question
    tk.Label(root, text=f"{num1} {op_symbol} {num2} = ?", font=("Comic Sans MS", 28, "bold"), 
             bg=BARNEY_PURPLE, fg=TEXT_COLOR).pack(pady=10)

    answer_entry = tk.Entry(root, font=("Comic Sans MS", 14), justify='center')
    answer_entry.pack(pady=5)
    answer_entry.focus()

    tk.Button(root, text="Submit Answer", command=check_answer, 
              font=("Comic Sans MS", 12), bg=BARNEY_GREEN).pack(pady=10)
    
    tk.Button(root, text="Menu", command=displayMenu, bg="tomato").pack(pady=5)


def check_answer():
    global score, current_question, attempt

    try:
        user_answer = float(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Oops!", "Please enter a number!")
        return

    if operation == "+": correct = num1 + num2
    elif operation == "-": correct = num1 - num2
    elif operation == "*": correct = num1 * num2
    elif operation == "/": correct = num1 / num2

    if abs(user_answer - correct) < 0.01:
        # CORRECT
        if attempt == 1: score += 10
        else: score += 5
        
        messagebox.showinfo("Correct!", "Super! Points for you!")
        current_question += 1
        attempt = 1
        
        if current_question > 10: displayResults()
        else: displayProblem()

    else:
        # WRONG: TRANSFORM!
        root.configure(bg=ERROR_RED)
        
        # Change Barney to T-Rex
        scary_photo = load_and_resize_image(SCARY_IMG_PATH, 220, 260)
        if scary_photo:
            image_label.configure(image=scary_photo, bg=ERROR_RED)
            image_label.image = scary_photo

        root.update()
        
        if attempt == 1:
            attempt += 1
            # "Slap" warning
            messagebox.showwarning("WRONG", "I hear a growl on the distance...\nTry again.")
            
            # Reset visuals
            root.configure(bg=BARNEY_PURPLE)
            happy_photo = load_and_resize_image(HAPPY_IMG_PATH, 180, 220)
            image_label.configure(image=happy_photo, bg=BARNEY_PURPLE)
            image_label.image = happy_photo
        else:
            messagebox.showerror("FAIL", f"SMACK!\nAnswer: {correct:.2f}")
            current_question += 1
            attempt = 1
            if current_question > 10: displayResults()
            else: displayProblem()


def displayResults():
    clear_window()
    root.configure(bg=BARNEY_PURPLE)
    
    tk.Label(root, text="Quiz Complete!", font=("Comic Sans MS", 20, "bold"), 
             bg=BARNEY_PURPLE, fg="yellow").pack(pady=10)
    tk.Label(root, text=f"Final Score: {score} / 100", font=("Comic Sans MS", 16), 
             bg=BARNEY_PURPLE, fg="white").pack(pady=5)

    if score >= 60:
        final_img_path = HAPPY_IMG_PATH
        rank = "You survived! Great job!"
    else:
        final_img_path = SCARY_IMG_PATH
        rank = "Run."

    photo = load_and_resize_image(final_img_path, 250, 300)
    if photo:
        lbl = tk.Label(root, image=photo, bg=BARNEY_PURPLE)
        lbl.image = photo
        lbl.pack(pady=10)

    tk.Label(root, text=rank, font=("Comic Sans MS", 14, "italic"), 
             bg=BARNEY_PURPLE, fg="white").pack(pady=10)
    
    create_button("Play Again", displayMenu)
    create_button("Exit", root.quit, bg_color="tomato")


def start_quiz(level):
    global difficulty, current_question, score, attempt
    difficulty = level
    score = 0
    current_question = 1
    attempt = 1
    displayProblem()


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# --- Main Window ---
root = tk.Tk()
root.title("Barney's Math Adventure")
root.geometry("500x650")
root.configure(bg=BARNEY_PURPLE)
root.resizable(False, False)

# --- SETTING THE CUSTOM ICON (Replacing the Feather) ---
try:
    # 1. Load the Ruler image using Pillow
    icon_image = Image.open(RULER_IMG_PATH)
    # 2. Convert it to a format Tkinter understands
    photo_icon = ImageTk.PhotoImage(icon_image)
    # 3. Set it as the window icon
    root.iconphoto(False, photo_icon)
except Exception as e:
    print(f"Could not set icon: {e}")

displayMenu()
root.mainloop()
