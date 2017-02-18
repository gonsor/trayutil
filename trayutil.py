#!/usr/bin/python

"""
Copyright (c) 2017 Daniel May
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import json
import subprocess
from collections import OrderedDict

from PyQt5 import QtGui, QtWidgets


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "trayutil")
MENU_PATH = os.path.join(CONFIG_DIR, "menu.json")


class TrayAction(QtWidgets.QAction):
    def __init__(self, text, cmd, parent=None):
        super().__init__(text, parent)
        self.cmd = cmd

    def invoke(self):
        subprocess.call(self.cmd, shell=True)


class TrayUtil(QtWidgets.QSystemTrayIcon):
    def __init__(self, config, icon, parent=None):
        super().__init__(icon, parent)

        self.menu = QtWidgets.QMenu(parent)
        self.fillMenu(self.menu, config)
        self.setContextMenu(self.menu)
        self.activated.connect(lambda: self.menu.popup(QtGui.QCursor.pos()))

    def fillMenu(self, menu, config):
        with open(config, "r") as f:
            structure = json.load(f, object_pairs_hook=OrderedDict)

        def walk(submenu, node):
            for k, v in node.items():
                if type(v) is OrderedDict:
                    submenu = submenu.addMenu(k)
                    walk(submenu, v)
                    submenu = submenu.parentWidget()
                else:
                    action = TrayAction(k, v, submenu)
                    action.triggered.connect(action.invoke)
                    submenu.addAction(action)

        walk(menu, structure)

        # add an exit entry
        menu.addSeparator()
        exitAction = menu.addAction("Quit")
        exitAction.triggered.connect(lambda: sys.exit(0))


def main(menu_path, args):
    app = QtWidgets.QApplication(args)

    tu = TrayUtil(menu_path,
        QtGui.QIcon(os.path.join(SCRIPT_DIR, "tray.png"))
    )
    tu.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv)
    elif os.path.exists(MENU_PATH):
        main(MENU_PATH, sys.argv)
    else:
        print("No menu file supplied. Quitting.")
