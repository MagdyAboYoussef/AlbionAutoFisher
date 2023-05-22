import cv2
import numpy as np
import pyautogui
import threading
from pydub import AudioSegment
from pydub.playback import play
from time import sleep
import helper
import os
import sys

with open('temp_file.txt', 'r') as f:
    temp_file_name = f.read().strip()

song = AudioSegment.from_wav("resources/warning.wav")
game_window = helper.get_game_window('Albion Online Client')

game_dimensions = {
    'y_top': game_window.top,
    'y_bot': game_window.bottom,
    'x_top': game_window.left,
    'x_bottom': game_window.right
}
# Define region dimensions for the 4 edges
edge_width = 50
x_top = game_dimensions['x_top']
x_bottom = game_dimensions['x_bottom']
y_top = game_dimensions['y_top']
y_bot = game_dimensions['y_bot']

left_region = (x_top, y_top, 150, y_bot-y_top)
right_region = (x_bottom-150, y_top, 150, y_bot-y_top)
bottom_region = (x_top, y_bot-155, x_bottom-x_top, 160)
top_region = (x_top, y_top+30, x_bottom-x_top, 45)


with open('player_image_paths.txt', 'r') as file:
    player_image_path = file.readline().strip()
    player_top_image_path = file.readline().strip()


# Load the player image and convert it to grayscale
player = cv2.imread(player_image_path, cv2.IMREAD_GRAYSCALE)
player_top = cv2.imread(player_top_image_path, cv2.IMREAD_GRAYSCALE)

# Define the template matching method to use
method = cv2.TM_CCOEFF_NORMED

# Define a threshold for the similarity score
threshold = 0.82


# Define a function for performing template matching in a given region

def match_template(region, result, player_image):
    # Take a screenshot of the region
    screenshot = np.array(pyautogui.screenshot(region=region))
    # Convert the screenshot to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Perform template matching for the player image against the region
    result[0] = (cv2.matchTemplate(gray, player_image, method), gray)  # return matchTemplate result and gray

    
while True:
    if not os.path.exists(temp_file_name):
        # The temp file has been deleted, stop the script
        sys.exit()


    # Define a list to hold the results of template matching for each region
    results = [None, None, None, None]

    # Define a list of threads for performing template matching in parallel
    threads = []

    # Create a thread for each region
    for i, region in enumerate([left_region, right_region, bottom_region, top_region]):
        result = [None]
        results[i] = result
        if i !=3:
            thread = threading.Thread(target=match_template, args=(region, result,player))
        else:
            thread = threading.Thread(target=match_template, args=(region, result,player_top))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Extract the maximum similarity score for each region from the results
    max_vals = []
    for result in results:
        max_val, gray = result[0][0].max(), result[0][1]
        max_vals.append(max_val)


    if max_vals[0] > threshold:
        play(song)
        sleep(0.2)
    elif max_vals[1] > threshold:
        play(song)
        sleep(0.2)

    elif max_vals[2] > threshold:
        play(song)
        sleep(0.2)

    elif max_vals[3] > 0.9:
        play(song)
        sleep(0.2)
