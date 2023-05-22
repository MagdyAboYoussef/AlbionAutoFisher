import pyautogui
import cv2
import numpy as np
from time import sleep
from pynput.mouse import Button, Controller
import keyboard
import math
import win32api
import pygetwindow as gw
import os
import sys
import helper
max_duration = 1.5
min_duration = 0
n= 0
mouse = Controller()

# Define the coordinates of the top-left and bottom-right corners of the squarex1_ratio = 830 / 1920


# Read the image paths from the file
with open('image_paths.txt', 'r') as file:
    bobber_image_path = file.readline().strip()
    bait_image_path = file.readline().strip()
    invis_image_path = file.readline().strip()



game_window = helper.get_game_window('Albion Online Client')
character_position = (game_window.width / 2, game_window.height / 2)

# Calculate the actual coordinates within the game window
width = game_window.right - game_window.left
height = game_window.bottom - game_window.top
x1_ratio = 830 / 1920
y1_ratio = 400 / 800
x2_ratio = 1080 / 1920
y2_ratio = 500 / 800
x1 = int(x1_ratio * width)
y1 = int(y1_ratio * height)
x2 = int(x2_ratio * width)
y2 = int(y2_ratio * height) 
image_width = x2 - x1
threshold = int(0.60 * image_width)
x1 += game_window.left
x2 += game_window.left
y1 += game_window.top
y2 += game_window.top

# Define the region to capture
region = (x1, y1, x2 - x1, y2 - y1)
bobber = cv2.imread(bobber_image_path, cv2.IMREAD_UNCHANGED)
gray_bobber = cv2.cvtColor(bobber, cv2.COLOR_BGR2GRAY)


bait = cv2.imread(bait_image_path, cv2.IMREAD_UNCHANGED)
gray_bait = cv2.cvtColor(bait, cv2.COLOR_BGR2GRAY)
invis = cv2.imread(invis_image_path, cv2.IMREAD_UNCHANGED)
gray_invis = cv2.cvtColor(invis, cv2.COLOR_BGR2GRAY)

started= False




def refill_bait():
    invX1 = game_window.left + int(width * 0.8)  # Starting from 80% width from the left
    invY1 = game_window.top  # Starting from the top
    invX2 = game_window.right  # Continuing to the end of the game window
    invY2 = game_window.bottom  # Continuing to the bottom of the game window

    right_region = (invX1, invY1, invX2-invX1, invY2-invY1)  # Region for the screenshot
    screenshot = np.array(pyautogui.screenshot(region = right_region))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  
    invScreen = cv2.imread("resources/inventory.png", cv2.IMREAD_GRAYSCALE)  

    inventory = cv2.matchTemplate(invScreen, screenshot_gray, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(inventory)
    if max_val<0.9:
        keyboard.press("i")
        sleep(0.15)
        keyboard.release("i")
    screenshot = np.array(pyautogui.screenshot(region = right_region))
  
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(
    gray_bait, gray_screenshot, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    adjusted_max_loc = (max_loc[0]+invX1+50, max_loc[1]+invY1+20)
    pyautogui.moveTo(*adjusted_max_loc)

    sleep(0.15)
    mouse.press(Button.right)
    mouse.release(Button.right)
    sleep(0.15)
    keyboard.press("f")
    sleep(0.15)
    keyboard.release("f")


    screenshot = np.array(pyautogui.screenshot())
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    sleep(0.1)
    result = cv2.matchTemplate(
    gray_invis, gray_screenshot, cv2.TM_CCOEFF_NORMED)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(result)
    adjusted_max_loc = (max_loc[0]+invX1+50, max_loc[1]+invY1+20)
    pyautogui.moveTo(*adjusted_max_loc)
    sleep(0.1)
    mouse.press(Button.right)
    mouse.release(Button.right)
    sleep(0.1)
    keyboard.press("i")
    sleep(0.1)
    keyboard.release("i")

def calculate_throw_duration(character_position, mouse_position, game_window, min_duration, max_duration):
    dx = mouse_position[0] - character_position[0]
    dy = mouse_position[1] - character_position[1]
    distance = math.sqrt(dx**2 + dy**2)

    # Adjust duration factor based on distance in x and y directions
    x_distance_factor = abs(dx) / game_window.width
    y_distance_factor = abs(dy) / game_window.height
    duration_factor = 1.0 + (x_distance_factor + y_distance_factor) / 2.0

    # Adjust duration based on mouse position
    if mouse_position[1] > character_position[1]:
        duration_factor *= 0.7

    duration = min_duration + (max_duration - min_duration) * distance / game_window.height
    duration = round(duration * duration_factor, 2)

    if duration <= 0.2:
        duration = 0
    elif duration <0.3:
        duration = duration*0.8

    return duration


def throwOnce():
    keyboard.press("s")
    keyboard.release("s")
    mouse.press(Button.left)
    sleep(calculate_throw_duration(character_position, mouse.position, game_window, min_duration, max_duration))
    mouse.release(Button.left)

with open('temp_file.txt', 'r') as f:
    temp_file_name = f.read().strip()


while True:
    # if not os.path.exists(temp_file_name):
    #     # The temp file has been deleted, stop the script
    #     sys.exit()
    if win32api.GetKeyState(0x06)<0:
        refill_bait()

    if win32api.GetKeyState(0x05)<0:
        throwOnce()
    # Capture the screenshot and convert it to a NumPy array
    screenshot = np.array(pyautogui.screenshot(region=region))
    # Process the screenshot using cv2
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(
        gray_bobber, gray_screenshot, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > 0.75:
        mouse.press(Button.left)
        started = True
        screenshot2 = np.array(pyautogui.screenshot(region=region))
        gray_screenshot2 = cv2.cvtColor(
            screenshot2, cv2.COLOR_BGR2GRAY)
        blobResult = cv2.matchTemplate(
            gray_bobber, gray_screenshot2, cv2.TM_CCOEFF_NORMED)
        min_valB, max_valB, min_locB, max_locB = cv2.minMaxLoc(
            blobResult)
        if max_locB[0] > threshold:
            mouse.release(Button.left)
            sleep(0.1)
            mouse.press(Button.left)
    elif max_val <0.75 and started == True:
        started = False
        mouse.release(Button.left)
        keyboard.press("s")
        sleep(0.1)
        keyboard.release("s")
        sleep(0.2)
        throwOnce()

