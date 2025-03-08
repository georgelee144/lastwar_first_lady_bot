import time
import pyautogui
import pytesseract
import yaml
import random
import re

def read_config(config_file):
    with open(config_file) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return

def approve_applicants_for_position(important_boxes):

    list_position = important_boxes["list_position"]
    approve_postion = important_boxes["approve_postion"]
    exit_position = important_boxes["exit_position"]

    pyautogui.click(list_position["x"], list_position["y"])
    time.sleep(random.uniform(0.5, 1.0))

    for _ in range(5):

        pyautogui.click(approve_postion["x"], approve_postion["y"])
        time.sleep(0.5)

    pyautogui.click(exit_position["x"], exit_position["y"])

    return

def dismiss_current_title_holders(the_config):

    important_boxes = the_config["important_boxes"]

    dismiss_position = important_boxes["dismiss_position"]
    dismiss_confirmation = important_boxes["dismiss_confirmation"]

    pyautogui.click(dismiss_position["x"], dismiss_position["y"])
    time.sleep(0.5)
    pyautogui.click(dismiss_confirmation["x"], dismiss_confirmation["y"])

    return

def clean_and_get_seconds(text_str):
    time_match = re.search(r'\d{2}:\d{2}:\d{2}', text_str)
    
    if time_match:
        time_extracted = time_match.group()
        str_parts = time_extracted.split(":")
        time_in_secs = 0

        for index,str_part in enumerate(str_parts):
            if index == len(str_parts) - 1:
                time_in_secs = time_in_secs + int(str_part)
            else:
                time_in_secs = 60 * (time_in_secs + int(str_part))
        return time_in_secs

    else:

        alternative_time_match = re.search(r'\d{2}:', text_str)
        if alternative_time_match:
            return -1
        else:
            return 0

def check_stale_role(region_to_screenshot,pytesseract_path,stale_timer):

    screenshot = pyautogui.screenshot(region=region_to_screenshot)
    # screenshot.save("text.png")

    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789:'
    text = pytesseract.image_to_string(screenshot,config=custom_config)

    seconds = clean_and_get_seconds(text)
    if seconds > stale_timer or seconds==-1:
        return True
    else:
        return False

def dismiss_stale_roles(the_config,stale_timer):
    
    time.sleep(1.5)

    region_to_screenshot = the_config["time_in_office_screenshot_region"]
    pytesseract_path = the_config["pytesseract_path"]
    stale_role_truth = check_stale_role(region_to_screenshot=region_to_screenshot,pytesseract_path=pytesseract_path,stale_timer=stale_timer)
    # print(stale_role_truth)
    if stale_role_truth:
        dismiss_current_title_holders(the_config)

    return

def the_bot(the_config):

    important_boxes = the_config["important_boxes"]
    safety_reset = important_boxes["safety_reset_position"]
    secretary_positions = the_config["secretary_positions"]
    exit_position = important_boxes["exit_position"]

    if the_config["conqueror_status"]:
        x_to_use = "conqueror_x"
        y_to_use = "conqueror_y"

        if the_config["conquered"]:
            del secretary_positions["military_commander"]
            del secretary_positions["adminstrative_commander"]
    else:
        x_to_use = "x"
        y_to_use = "y"

    time.sleep(5)

    while True:
        for _,coordinates in secretary_positions.items():

            if not coordinates.get(x_to_use):
                continue

            pyautogui.click(coordinates[x_to_use], coordinates[y_to_use])
            # print(_,coordinates[x_to_use], coordinates[y_to_use])
            time.sleep(0.5)

            approve_applicants_for_position(important_boxes=important_boxes)
            time.sleep(0.1)
            pyautogui.click(safety_reset["x"], safety_reset["y"])
            time.sleep(5)

            if the_config["dismiss_position_stale_positions"]:
                pyautogui.click(coordinates[x_to_use], coordinates[y_to_use])
                if coordinates["stale_timer"] is None or coordinates["stale_timer"] == 0:
                    pass
                else:

                    dismiss_stale_roles(the_config=the_config,stale_timer=coordinates["stale_timer"])
                pyautogui.click(exit_position["x"], exit_position["y"])
                time.sleep(0.1)
                pyautogui.click(safety_reset["x"], safety_reset["y"])
                time.sleep(5)
    return

if __name__ == "__main__":
    the_config = read_config("first_lady_config.yaml")
    time.sleep(3)
    the_bot(the_config)
    