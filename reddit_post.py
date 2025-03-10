# from https://www.reddit.com/r/LastWarMobileGame/comments/1ehbeuw/comment/lpekuyk/

import pyautogui
import time
import re   
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Start script on server's position selection screen. 
# NOTE: if conquerors buff is enabled, scroll down before running.

# Function to convert HH:mm:ss to total minutes
def time_to_minutes(time_str):
    hours, minutes, _ = map(int, time_str.split(':'))
    return hours * 60 + minutes


def text_sanitization(time_str):
    if not time_str:
        return ''
    if time_str[:3].isdigit():
        time_str = time_str[1:] # Remove extra leading digit
    parts = time_str.split(':')
    if len(parts[2]) > 2:
        parts[2] = parts[2][:2]  # Remove extra trailing digit
    return ':'.join(parts)

def remove_stale_roles(left, top, width, height, message, x, y):
    # Define the region to capture (left, top, width, height)
    region = (left, top, width, height)
    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)
    # Convert the screenshot to a format suitable for pytesseract
    screenshot_rgb = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)

    # Define OCR configuration options
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789:'

    # Extract text with custom configuration
    text = text_sanitization(pytesseract.image_to_string(screenshot_rgb, config=custom_config))
    # Use regular expression to find time strings in HH:mm:ss format
    pattern = r'\b\d{2}:\d{2}:\d{2}\b'
    matches = re.findall(pattern, text)
    # Threshold in minutes
    threshold_minutes = 6
    if matches is None:
        print("{message} Screenshot returned NULL list.")
    elif not matches:
        print(f"{message} Screenshot returned no matches. Text: {text}")
    else:
        # Threshold in minutes
        total_minutes = time_to_minutes(matches[0])
        if total_minutes >= threshold_minutes:
            print(f"{matches[0]} {message} is greater than {threshold_minutes} minutes.")
            pyautogui.click(x, y) # click given title card
            time.sleep(.6)
            pyautogui.click(2117, 935) # click dismiss
            time.sleep(.6)
            pyautogui.click(2108, 610) # click Confirm
            time.sleep(.6)
            # exit position card
            exitX = 2185
            exitY = 1079
            pyautogui.click(exitX, exitY)
            time.sleep(.6)
            pyautogui.click(exitX, exitY)
            time.sleep(.6)
        else:
            print(f"{message} is less than {threshold_minutes} minutes.")



def approve_applicant_list(x, y):
    # Click the position card from given coordinates.
    # click the approve button location a few times. Then exit out of the position card.
    clickSeconds1 = .65
    clickSeconds2 = .35

    # click position card
    pyautogui.click(x, y)
    time.sleep(clickSeconds1)
    # click list button
    listX = 2447
    listY = 951
    pyautogui.click(listX, listY)
    time.sleep(clickSeconds1)
    # click approve
    approveX = 2371
    approveY = 288
    for i in range(3):
        pyautogui.click(approveX, approveY)
        time.sleep(clickSeconds2)
    # exit position card
    exitX = 2185
    exitY = 1079
    pyautogui.click(exitX, exitY)
    time.sleep(clickSeconds2)
    pyautogui.click(exitX, exitY)
    time.sleep(clickSeconds1)
    return True

def main():
    # Conquerors Buff includes two additional position cards. Set to False if conquerors buff is disabled.
    conquerorsBuff = True
    # list of coordinates for each position card, ordered Mil Cmdr to Sec Interior top left to bottom right
    if conquerorsBuff:
        coordinates = [
            (2109, 441), # Military Commander
            (2316, 425), # Administration Commander
            (2212, 677), # Secretary of Strategy...
            (2396, 636),
            (2053, 973),
            (2209, 850), # Note, a player liking the bot's profile makes a permanent screen appear. This may be exited via the "Awesome" button.
            (2383, 955)
        ]

        staleRoleCoordinates = [
            (2078, 485, 104, 25, 'Military Commander', 2109, 441),
            (2184, 718, 104, 25, 'Secretary of Strategy', 2212, 677),
            (2366, 718, 104, 25, 'Secretary of Security', 2396, 636),
            (2002, 951, 104, 25, 'Secretary of Development', 2053, 973),
            (2184, 951, 104, 25, 'Secretary of Science', 2209, 850)
        ]
    else:
        coordinates = [
            (2212, 535), # Secretary of Strategy...
            (2397, 545),
            (2025, 770),
            (2209, 850), # Note, a player liking the bot's profile makes a permanent screen appear. This may be exited via the 'Awesome' button.
            (2398, 769)
        ]
        staleRoleCoordinates = [
            (2359, 627, 104, 40, 'Secretary of Security', 2397, 545),
            (2175, 629, 104, 40, 'Secretary of Strategy', 2212, 535)
        ]
    time.sleep(5) # giving time to get screen ready
    i = 9
    while True:
        i = i + 1
        # Iterate through the positions and approve all
        for x, y in coordinates:
            action = approve_applicant_list(x, y)
        if i % 10 == 0:
            # Iterate through positions to check for stale activity
            for left, top, width, height, message, x, y in staleRoleCoordinates:
                remove_stale_roles(left, top, width, height, message, x, y)
        time.sleep(4) # giving operator time to stop the script
    

if __name__ == "__main__":
    main()
