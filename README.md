Hello from 704!

This is a First Lady or Vice President bot for the mobile game Last War. This bot replaces the need for a human to manually approve and remove players from different secretary position as it is a tedious task no one should be subjected to.

## Steps to run
1. Download a virtual machine (VM) and phone/tablet emulator inside of the VM of your choice. I was using QEMU/KVM to launch a Windows 10 VM and used BlueStacks as my emulator. A VM is not necessary but is recommended since the script takes over your inputs (mouse).

2. Download this repository (repo).

    ```git clone https://github.com/georgelee144/lastwar_first_lady_vice_president_bot.git```

3. Change into the newly create directory and create a local python environment (env). It is always recommended to make a new env for any project you are working in.

    ```cd lastwar_first_lady_bot```
    
    Use whatever is your favorite python package manager. I recommend [uv](https://docs.astral.sh/uv/guides/) or base python very own venv.
    
    ```python -m venv .```

4. Download the necessary packages and program. You will also need to visit https://tesseract-ocr.github.io/tessdoc/Downloads.html to download a model that can extract text from images. If you just want to auto approve function then you can skip this but you will need to comment out the appropriate lines.
    
    If you are using uv then run this command.
    
    ```uv install```

    If you are using some other python package manager then run this.

    ```pip install -r requirements.txt```

    Activate your env, depending on your OS this is a bit different for everyone.

5. Run your emulator, Last War mobile game, and also `find_mouse_position.py`. This script will display your x,y coordinates of your cursor and you will need to change `first_lady_config.yaml` according to your setup. Get yourself to the secretary selection screen and fill out the yaml file accordingly. If you want to skip most of that work ... My settings was windows 10, resolution of 1280x768 with 100% scale. BlueStacks Emulator `2 CPU allocation`, `4 GB Memory allocation`, `Balanced Performance mode`, `Landscape`, `960 x 540` at `240 dpi`, `25 fps`, and `100% scale`.
    
   The coordinates for `time_in_office_screenshot_region` needs to capture ![alt text](image.png)

   `conqueror_x` and `conqueror_y` positions are different from just `x` and `y` conqueror_x or conqueror_y is for when capitol has been captured.

   `stale_timer` is time in seconds, by default most positions will be 7 minutes (420 seconds).

6. Run `first_lady_bot.py` to test and repeat the previous step if you have issues.
