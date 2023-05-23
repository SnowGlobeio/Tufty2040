#Snowglobe Badge V0.1 Remasterized
import Display
import Event
import setting
import time
import jpegdec
import qrcode


WIDTH, HEIGHT = display.get_bounds()

# Some constants we'll use for drawing
BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40

    # Draw QR button label
    display.set_pen(LIGHTEST)
    display.text("QR", 240, 215, 160, 2)


# draw the badge for the first time

draw_badge()
show_photo()
display.update()

while True:
	if badge_mode == "photo":
		draw_badge()
        show_photo()
        display.update()
	    if button_c.is_pressed:
            badge_mode = "qr"
            show_qr()
            display.update()
    time.sleep(1) 
