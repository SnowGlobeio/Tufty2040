import gc
from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
from os import listdir
import math, random, time
import display

#display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)
selected_item = 2
scroll_position = 2
target_scroll_position = 2

applications = []
affapp = []
appnotshow = ["main.py","display.py","lux.py","file.py","bat.py","menu.py"]
def text(text, x, y, pen, s):
    display.set_pen(pen)
    display.text(text, x, y, -1, s)
    

def get_applications():
    # fetch a list of the applications that are stored in the filesystem
    for file in listdir():
        #if file.endswith(".py") and file != "main.py":
        if file.endswith(".py") and file not in appnotshow:    
            # convert the filename from "something_or_other.py" to "Something Or Other"
            # via weird incantations and a sprinkling of voodoo
            title = " ".join([v[:1].upper() + v[1:] for v in file[:-3].split("_")])
            applications.append(
                {
                    "file": file,
                    "title": title
                }
            )          
    # sort the application list alphabetically by title and return the list
    return sorted(applications, key=lambda x: x["title"])


def launch_application(application):
    #wait_for_user_to_release_buttons()
    for k in locals().keys():
        if k not in ("gc", "file", "badger_os"):
            del locals()[k]
    gc.collect()
    __import__(application["file"])
