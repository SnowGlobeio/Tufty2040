import event, display, bat
import time
from lux import *

# draw the badge for the first time
badge_mode = "photo"
display.draw_badge()
display.show_photo()
display.update()

backlight = BACKLIGHT_LOW
while True:
    display.t = time.ticks_ms() / 800.0
    lux_vref_pwr.value(1)
    (vbat, on_usb, low_battery) = measure_battery()
    bat.measure_battery()
    if low_battery:
        backlight = BACKLIGHT_LOW
    else:
        (luminance, backlight) = auto_brightness(backlight)
    lux_vref_pwr.value(0)
    display.set_backlight(backlight)
    if badge_mode == "photo":
        display.draw_badge()
        display.hightext()
        display.show_photo()
        #display.hightext()
        display.update()
    
    if badge_mode == "bat":
        display.bmode_status_tick()
    
    if event.button_c.is_pressed:
        if badge_mode == "photo":
            badge_mode = "qr"
            display.show_qr()
            display.update()
        else:
            badge_mode = "photo"
            display.draw_badge()
            display.show_photo()
            display.update()
        time.sleep(1)
    if event.button_a.is_pressed:
        if badge_mode != "bat" or "qr":
          __import__("menu.py")
    if event.button_b.is_pressed:
        if badge_mode == "photo":
            badge_mode = "bat"
            display.clear()
            display.bmode_status_tick()
        else:
            badge_mode = "photo"
            display.draw_badge()
            display.show_photo()
            display.update()
        time.sleep(1)
