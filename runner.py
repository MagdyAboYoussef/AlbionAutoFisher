import tkinter as tk
from tkinter import filedialog
import threading    
import os
import subprocess
import tempfile

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Images")
        self.root.geometry("500x500")
        self.temp_file_name = None
        self.blobber_image = "resources/blobber.png"
        self.bait_image = "resources/bait.png"
        self.invis_image = "resources/invis.png"

        self.script1 = None
        self.script2 = None
        self.script3 = None
        self.blobber_button = tk.Button(self.root, text="Select Bobber Image", command=self.get_blobber_image)
        self.blobber_button.pack()

        self.bait_button = tk.Button(self.root, text="Select Bait Image", command=self.get_bait_image)
        self.bait_button.pack()

        self.invis_button = tk.Button(self.root, text="Select Invis Image", command=self.get_invis_image)
        self.invis_button.pack()

        self.player_image = "resources/playerBot.png"
        self.player_top_image = "resources/playerTop.png"

        self.player_button = tk.Button(self.root, text="Select Image for Player bar at Bottom of screen ", command=self.get_player_image)
        self.player_button.pack()

        self.player_top_button = tk.Button(self.root, text="Select Image for Player at Top of screen", command=self.get_player_top_image)
        self.player_top_button.pack()

        self.sound_check = tk.BooleanVar() 
        self.helper_check = tk.BooleanVar() 

        sound_check_button = tk.Checkbutton(self.root, text='Click when fish bite sound', var=self.sound_check)
        helper_check_button = tk.Checkbutton(self.root, text='Run edge screen player detection(not recommended)', var=self.helper_check)

        sound_check_button.pack()
        helper_check_button.pack()
        self.stop_button = tk.Button(self.root, text='Stop', command=self.stop_scripts)
        self.stop_button.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_script)
        self.start_button.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_blobber_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file:
            self.blobber_image = file

    def get_bait_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file:
            self.bait_image = file

    def get_invis_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file:
            self.invis_image = file

    def get_player_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file:
            self.player_image = file

    def get_player_top_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file:
            self.player_top_image = file

    def run_script1(self):
        subprocess.Popen(['python', 'player.py'])

    def run_script2(self):
        subprocess.Popen(['python', 'fishing.py'])

    def run_script3(self):
        subprocess.Popen(['python', 'sound.py'])

    def start_script(self):
        with open('temp_file.txt', 'w') as f:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            f.write(temp_file.name)
            # update self.temp_file_name
            self.temp_file_name = temp_file.name
        with open('image_paths.txt', 'w') as file:
            file.write(f"{self.blobber_image}\n")
            file.write(f"{self.bait_image}\n")
            file.write(f"{self.invis_image}\n")

        with open('player_image_paths.txt', 'w') as file:
            file.write(f"{self.player_image}\n")
            file.write(f"{self.player_top_image}\n")

        self.script1 = None
        self.script2 = None
        self.script3 = None

        if self.sound_check.get():
            self.script3 = subprocess.Popen(['python', 'sound.py'])

        if self.helper_check.get():
            self.script1 = subprocess.Popen(['python', 'player.py'])

        self.script2 = subprocess.Popen(['python', 'fishing.py'])
        
        self.start_button.config(state=tk.DISABLED)





    def stop_scripts(self):
        # stop all scripts
        if self.script1 is not None:
            self.script1.terminate()
        if self.script2 is not None:
            self.script2.terminate()
        if self.script3 is not None:
            self.script3.terminate()
        self.start_button.config(state=tk.NORMAL)

    def on_close(self):
        self.stop_scripts()
        if self.temp_file_name is not None:
            if os.path.exists(self.temp_file_name):
                os.remove(self.temp_file_name)
        self.root.destroy()


root = tk.Tk()
app = App(root)
root.mainloop()
