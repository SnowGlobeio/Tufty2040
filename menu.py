import math, random, time
import display, event, file
from file import applications


applications = file.get_applications()

#display.set_backlight()

selected_item = 2
scroll_position = 2
target_scroll_position = 2

while True:
    display.t = time.ticks_ms() / 1000.0
        
    if event.button_up.read():
        target_scroll_position -= 1
        target_scroll_position = target_scroll_position if target_scroll_position >= 0 else len(applications) - 1

    if event.button_down.read():
        target_scroll_position += 1
        target_scroll_position = target_scroll_position if target_scroll_position < len(applications) else 0

    if event.button_a.read():
        file.launch_application(applications[selected_item])
        
    display.clear()
    
    scroll_position += (target_scroll_position - scroll_position) / 5
    
    display.grid()
            
    # work out which item is selected (closest to the current scroll position)
    selected_item = round(target_scroll_position)

    start = time.ticks_ms()
    
    display.listapp(applications, scroll_position, selected_item)

    start = time.ticks_ms()
    
    display.update()
