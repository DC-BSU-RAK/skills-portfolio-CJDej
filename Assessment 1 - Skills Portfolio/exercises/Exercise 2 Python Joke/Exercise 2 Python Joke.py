import tkinter as tk
from tkinter import font
import random
import os
from PIL import Image, ImageTk 
import pygame 

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Joke Bot ʕ•͡•ʔ")
        self.root.geometry("600x500")

        # --- PATH SETUP (Fixes the "Blue Feather" issue) ---
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # --- 1. SETTING THE ICON ---
        icon_path = os.path.join(self.base_path, "Laughing.jpg")
        if os.path.exists(icon_path):
            try:
                self.icon_image = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(False, self.icon_image)
            except Exception as e:
                print(f"Error loading icon: {e}")
        else:
            print("Warning: Icon not found. Make sure 'Laughing.jpg' is in the folder.")

        # --- 2. AUDIO SETUP ---
        pygame.mixer.init()

        # Load Sound Effect
        self.laugh_sound = None
        sound_path = os.path.join(self.base_path, "let-me-know.mp3")
        
        if os.path.exists(sound_path):
            try:
                self.laugh_sound = pygame.mixer.Sound(sound_path)
                self.laugh_sound.set_volume(0.5) 
            except Exception as e:
                print(f"Error loading laugh: {e}")

        # Load Background Music
        music_path = os.path.join(self.base_path, "05. Elevator Jam.mp3")
        
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                
                # --- CHANGE 1: LOWER VOLUME ---
                pygame.mixer.music.set_volume(0.1)  # Changed from 0.3 to 0.1
                
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error loading music: {e}")
        
        # --- UI COLORS ---
        self.bg_color = "#120520"       
        self.frame_bg = "#2A0E45"       
        self.text_color = "#E0B0FF"     
        self.neon_green = "#39FF14"     
        self.button_bg = "#5D2E8C"      
        self.button_fg = "#FFFFFF"      
        self.quit_bg = "#800000"        
        
        self.root.configure(bg=self.bg_color)

        self.jokes = [
            ("Why did the chicken cross the road?", "To get to the other side."),
            ("What happens if you boil a clown?", "You get a laughing stock."),
            ("Why did the car get a flat tire?", "Because there was a fork in the road!"),
            ("How did the hipster burn his mouth?", "He ate his pizza before it was cool."),
            ("What did the janitor say when he jumped out of the closet?", "SUPPLIES!!!!"),
            ("Have you heard about the band 1023MB?", "It's probably because they haven't got a gig yet…"),
            ("Why does the golfer wear two pants?", "Because he's afraid he might get a 'Hole-in-one.'"),
            ("Why should you wear glasses to maths class?", "Because it helps with division."),
            ("Why does it take pirates so long to learn the alphabet?", "Because they could spend years at C."),
            ("Why did the woman go on the date with the mushroom?", "Because he was a fun-ghi."),
            ("Why do bananas never get lonely?", "Because they hang out in bunches."),
            ("What did the buffalo say when his kid went to college?", "Bison."),
            ("Why shouldn't you tell secrets in a cornfield?", "Too many ears."),
            ("What do you call someone who doesn't like carbs?", "Lack-Toast Intolerant."),
            ("Why did the can crusher quit his job?", "Because it was soda pressing."),
            ("Why did the birthday boy wrap himself in paper?", "He wanted to live in the present."),
            ("What does a house wear?", "A dress."),
            ("Why couldn't the toilet paper cross the road?", "Because it got stuck in a crack."),
            ("Why didn't the bike want to go anywhere?", "Because it was two-tired!"),
            ("Want to hear a pizza joke?", "Nahhh, it's too cheesy!"),
            ("Why are chemists great at solving problems?", "Because they have all of the solutions!"),
            ("Why is it impossible to starve in the desert?", "Because of all the sand which is there!"),
            ("What did the cheese say when it looked in the mirror?", "Halloumi!"),
            ("Why did the developer go broke?", "Because he used up all his cache."),
            ("Did you know that ants are the only animals that don't get sick?", "It's true! It's because they have little antibodies."),
            ("Why did the donut go to the dentist?", "To get a filling."),
            ("What do you call a bear with no teeth?", "A gummy bear!"),
            ("What does a vegan zombie like to eat?", "Graaains."),
            ("What do you call a dinosaur with only one eye?", "A Do-you-think-he-saw-us!"),
            ("Why should you never fall in love with a tennis player?", "Because to them... love means NOTHING!"),
            ("What did the full glass say to the empty glass?", "You look drunk."),
            ("What's a potato's favorite form of transportation?", "The gravy train."),
            ("What did one ocean say to the other?", "Nothing, they just waved."),
            ("What did the right eye say to the left eye?", "Honestly, between you and me something smells."),
            ("What do you call a dog that's been run over by a steamroller?", "Spot!"),
            ("What's the difference between a hippo and a zippo?", "One's pretty heavy and the other's a little lighter."),
            ("Why don't scientists trust Atoms?", "They make up everything.")
        ]
        
        self.current_joke = None
        self.is_setup_shown = False

        self.header_font = font.Font(family="Courier New", size=24, weight="bold")
        self.setup_font = font.Font(family="Courier New", size=26, weight="bold")
        self.punchline_font = font.Font(family="Courier New", size=20, slant="italic")
        self.btn_font = font.Font(family="Courier New", size=12, weight="bold")
        
        self.header = tk.Label(root, text="ʕ•͡•ʔ JOKE QUEST ʕ•͡•ʔ", bg=self.bg_color, fg=self.neon_green, font=self.header_font)
        self.header.pack(pady=20)

        self.text_frame = tk.Frame(root, bg=self.frame_bg, bd=4, relief="ridge")
        self.text_frame.pack(pady=10, padx=40, fill="both", expand=True)

        self.setup_label = tk.Label(self.text_frame, text="PRESS START TO PLAY...", 
                                    font=self.setup_font, bg=self.frame_bg, fg=self.text_color, wraplength=500)
        self.setup_label.pack(pady=(40, 10), padx=20)

        self.punchline_label = tk.Label(self.text_frame, text="", 
                                        font=self.punchline_font, bg=self.frame_bg, fg="#FF00FF", wraplength=500)
        self.punchline_label.pack(pady=10, padx=20)

        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=30)

        self.action_button = tk.Button(self.button_frame, text="START GAME", command=self.handle_click,
                                       font=self.btn_font, bg=self.button_bg, fg=self.button_fg, 
                                       activebackground="#7B4AA8", activeforeground="white",
                                       relief="raised", bd=3, width=15, pady=5)
        self.action_button.pack(side="left", padx=10)

        self.quit_button = tk.Button(self.button_frame, text="QUIT GAME", command=root.destroy,
                                       font=self.btn_font, bg=self.quit_bg, fg="white", 
                                       activebackground="#FF0000", activeforeground="white",
                                       relief="raised", bd=3, width=15, pady=5)
        self.quit_button.pack(side="left", padx=10)

    def handle_click(self):
        """Handles the button click based on current state."""
        if not self.is_setup_shown:
            # State: Showing a new setup
            
            # --- CHANGE 2: STOP LAUGHING ---
            # If the user clicks NEXT, stop the previous laugh immediately
            if self.laugh_sound:
                self.laugh_sound.stop()
                
            self.get_new_joke()
            self.action_button.config(text="REVEAL ANSWER", bg="#ff9900") 
            self.is_setup_shown = True
        else:
            # State: Showing the punchline
            self.show_punchline()
            self.action_button.config(text="NEXT LEVEL", bg=self.button_bg) 
            self.is_setup_shown = False
            
            if self.laugh_sound:
                self.laugh_sound.stop() # Stop any overlapping sounds
                self.laugh_sound.play()

    def get_new_joke(self):
        """Selects a random joke and displays the setup."""
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0])
        self.punchline_label.config(text="")  

    def show_punchline(self):
        """Displays the punchline of the current joke."""
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()