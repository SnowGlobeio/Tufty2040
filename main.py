import event, display, bat
import time

# draw the badge for the first time
badge_mode = "photo"
display.draw_badge()
display.show_photo()
display.update()

while True:
    display.t = time.ticks_ms() / 1000.0
    display.clear()
    bat.measure_battery()
    if badge_mode == "photo":
        display.draw_badge()
        display.show_photo()
        display.hightext()
        

        display.update()
    
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
        __import__("menu.py")
    if event.button_b.is_pressed:
        if badge_mode == "photo":
            badge_mode = "bat"
            display.clear()
            bmode_status_tick()
        else:
            badge_mode = "photo"
            draw_badge()
            show_photo()
            display.update()
        time.sleep(1)
