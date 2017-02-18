# Trayutil

Trayutil is a traybar icon which shows a json defined menu when clicked. It can be used to quickly bind complex commands to
one-click menu entries.

## Usage

Either supply a menu.json file as a program parameter or create a ~/.config/trayutil/menu.json file.

## Example menu.json

```javascript
{
    "Hello World": "notify-send 'Hello World!' 'Hello World.' --icon=dialog-information",
    "Power": {
        "Reboot": "systemctl reboot",
        "Poweroff": "systemctl poweroff"
    }
}
```
