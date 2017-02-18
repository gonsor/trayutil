# Trayutil

Trayutil is a traybar icon which shows a json defined menu when clicked. It is written in Python 3 with PyQt5.
You can use it to quickly bind complex commands to one-click menu entries.

## Usage

Either supply a **menu.json** file as a program parameter or create a **~/.config/trayutil/menu.json** file. 

Every _"name": "command"_ entry in the json file creates a new menu entry that executes the command on click. You can also create as many submenus as you want.

## Example menu.json

    {
        "Hello World": "notify-send 'Hello World!' 'Hello World.' --icon=dialog-information",
        "Power": {
            "Reboot": "systemctl reboot",
            "Poweroff": "systemctl poweroff"
        }
    }

**Result**

![Example Menu](https://github.com/gonsor/trayutil/blob/master/screenshot.png)
