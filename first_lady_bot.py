import time
import pyautogui
import yaml
import random

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

def dismiss_current_title_holders(important_boxes):

    dismiss_position = important_boxes["dismiss_postion"]
    pyautogui.click(dismiss_position["x"], dismiss_position["y"])
    time.sleep(0.1)
    pyautogui.click(dismiss_position["x"], dismiss_position["y"])

    return

def dismiss_stale_roles(important_boxes):
    
    dismiss_current_title_holders(important_boxes)

    return

def the_bot(the_config):

    important_boxes = the_config["important_boxes"]
    safety_reset = important_boxes["safety_reset"]
    secretary_positions = the_config["secretary_positions"]

    if the_config["conqueror_status"]:
        x_to_use = "conqueror_x"
        y_to_use = "conqueror_y"

        if the_config["conquered"]:
            del secretary_positions["military_commander"]
            del secretary_positions["adminstrative_commander"]
    else:
        x_to_use = "x"
        y_to_use = "y"

    while True:
        for _,coordinates in secretary_positions.items():

            pyautogui.click(coordinates[x_to_use], coordinates[y_to_use])
            time.sleep(0.1)

            if the_config["dismiss_position_stale_positions"]:
                dismiss_stale_roles(important_boxes)

            approve_applicants_for_position(important_boxes)
            time.sleep(0.1)
            pyautogui.click(safety_reset["x"], safety_reset["y"])
            time.sleep(5)
        
    return

if __name__ == "__main__":
    the_config = read_config("first_lady_config.yaml")
    the_bot(the_config)
    