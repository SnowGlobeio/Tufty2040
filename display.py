# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.

from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import gc, math
import jpegdec
import qrcode
import micropython
import event
from bat import *

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)

WIDTH, HEIGHT = display.get_bounds()

def update():
    display.update()


def clear():
    display.set_pen(display.create_pen(50, 50, 50))
    display.clear()


BACKLIGHT_LOW = micropython.const(0.375)
BACKLIGHT_HIGH = micropython.const(1.0)

LUMINANCE_LOW = micropython.const(256)
LUMINANCE_HIGH = micropython.const(2048)  # 65535 to use the full range.

# Fursona reaction hysteresis thresholds are set much higher.
REACT_BRIGHT_SET   = micropython.const(32768)
REACT_BRIGHT_RESET = micropython.const(16384)


# Uncomment one of these four colour palettes - find more at lospec.com !
# Nostalgia colour palette by WildLeoKnight - https://lospec.com/palette-list/nostalgia
LIGHTEST = display.create_pen(255, 255, 255)
LIGHT = display.create_pen(134, 188, 209)
DARK = display.create_pen(49, 106, 150)
DARKEST = display.create_pen(46, 36, 63)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(200, 0, 0)


# Change your badge and QR details here!
#COMPANY_NAME = "LeHack KERNEL PANIC"
message = "Le Hack 2023 KERNEL PANIC !"
text_size = 3
message_width = display.measure_text(message, text_size)
NAME = "Snowglobe"
BLURB1 = "Web"
BLURB2 = "Twitter"
BLURB3 = ""

#QR_TEXT_SITE = "https://snowglobe.io/lehack2023"
QR_TEXT = "https://snowglobe.io/lehack2023"
QR_TEXT_TWITTER = "https://twitter.com/SnowGlobe_io"


IMAGE_NAME = "twitter.jpg"

# Some constants we'll use for drawing
BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40

XSCROLL = 320

# Constant for text selection
selected_pen = display.create_pen(255, 255, 255)
unselected_pen = display.create_pen(80, 80, 100)
background_pen = display.create_pen(50, 50, 70)
shadow_pen = display.create_pen(0, 0, 0)

# convert a hue, saturation, and value into rgb values
def hsv_to_rgb(h, s, v):
    if s == 0.0: return v, v, v
    i = int(h * 6.0)  
    f = (h * 6.0) - i
    p, q, t = v * (1.0 - s), v * (1.0 - s * f), v * (1.0 - s * (1.0 - f))
    v, t, p, q = int(v * 255), int(t * 255), int(p * 255), int(q * 255)
    i = i % 6
    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q
    

def update():
    display.update()
    

def draw_badge():
    # draw border
    display.set_pen(LIGHTEST)
    display.clear()

    # draw background
    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # draw company box
    display.set_pen(DARKEST)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), COMPANY_HEIGHT)

    # draw name text
    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(NAME, BORDER_SIZE + PADDING, BORDER_SIZE + PADDING + COMPANY_HEIGHT, WIDTH, 5)

    # draws the bullet points
    display.set_pen(DARKEST)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 105, 160, 2)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 140, 160, 2)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 175, 160, 2)

    # draws the blurb text (4 - 5 words on each line works best)
    display.set_pen(LIGHTEST)
    display.text(BLURB1, BORDER_SIZE + PADDING + 135 + PADDING, 105, 160, 2)
    display.text(BLURB2, BORDER_SIZE + PADDING + 135 + PADDING, 140, 160, 2)
    display.text(BLURB3, BORDER_SIZE + PADDING + 135 + PADDING, 175, 160, 2)
    
# Draw chunky 3D rectangles.
def draw_3d_rect(x, y, w, h, highlight, fill, shadow):
    display.set_pen(shadow)
    display.rectangle(x, y, w, h)
    display.set_pen(highlight)
    display.rectangle(x, y, w-2, h-2)
    display.set_pen(fill)
    display.rectangle(x+2, y+2, w-4, h-4)

def draw_text_centered(text, x, y, wordwrap, scale=2.0, spacing=1):
    w = display.measure_text(text, scale, spacing)
    display.text(text, int(x + ((wordwrap - w) / 2)), y, wordwrap,
                 scale=scale, spacing=spacing)


def draw_text_right(text, x, y, wordwrap, scale=2.0, spacing=1):
    w = display.measure_text(text, scale, spacing)
    display.text(text, x + (wordwrap - w), y, wordwrap,
                 scale=scale, spacing=spacing)

def show_photo():
    j = jpegdec.JPEG(display)

    # Open the JPEG file
    j.open_file(IMAGE_NAME)

    # Draws a box around the image
    display.set_pen(DARKEST)
    display.rectangle(PADDING, HEIGHT - ((BORDER_SIZE * 2) + PADDING) - 120, 120 + (BORDER_SIZE * 2), 85 + (BORDER_SIZE * 2))

    # Decode the JPEG
    j.decode(BORDER_SIZE + PADDING, HEIGHT - (BORDER_SIZE + PADDING) - 120)

    # Draw Menu button label
    display.set_pen(LIGHTEST)
    display.text("Menu", 50, 215, 160, 2)

    # Draw QR button label
    display.set_pen(LIGHTEST)
    display.text("QR-code", 240, 215, 160, 2)


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(LIGHTEST)
    display.rectangle(ox, oy, size, size)
    display.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def show_qr():
    display.set_pen(DARK)
    display.clear()
    #led.value(True) 
    code = qrcode.QRCode()
    code.set_text(QR_TEXT)

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)
    #led.value(False)
    
def bmode_status_tick():
    WPAL_BLACK    = micropython.const(0)
    WPAL_DRED     = micropython.const(1)
    WPAL_DGREEN   = micropython.const(2)
    WPAL_DYELLOW  = micropython.const(3)
    WPAL_DBLUE    = micropython.const(4)
    WPAL_DMAGENTA = micropython.const(5)
    WPAL_DCYAN    = micropython.const(6)
    WPAL_GREY     = micropython.const(7)
    WPAL_DGREY    = micropython.const(248)
    WPAL_RED      = micropython.const(249)
    WPAL_GREEN    = micropython.const(250)
    WPAL_YELLOW   = micropython.const(251)
    WPAL_BLUE     = micropython.const(252)
    WPAL_MAGENTA  = micropython.const(253)
    WPAL_CYAN     = micropython.const(254)
    WPAL_WHITE    = micropython.const(255)
    GAUGE_X           = micropython.const(56)
    GAUGE_VBAT_Y      = micropython.const(24)
    GAUGE_LUX_Y       = micropython.const(96)
    GAUGE_BACKLIGHT_Y = micropython.const(168)
    GAUGE_W           = micropython.const(256)
    GAUGE_H           = micropython.const(64)
    SCALE = micropython.const(2)

    display.set_pen(WPAL_BLACK)
    display.rectangle(GAUGE_X, GAUGE_VBAT_Y, GAUGE_W, GAUGE_H)
    display.rectangle(GAUGE_X, GAUGE_LUX_Y, GAUGE_W, GAUGE_H)
    display.rectangle(GAUGE_X, GAUGE_BACKLIGHT_Y, GAUGE_W, GAUGE_H)

    # Battery gauge debugging for while attached to Thonny.
    if False:
        stats["usb"] = False
        stats['vbat_low'] = 3.0
        stats['vbat'] -= 0.01
        stats['vbat_high'] = 3.8
        if stats['vbat'] < VBAT_LOW:
            stats['vbat'] = VBAT_HIGH

    if stats["usb"]:
        display.set_pen(WPAL_WHITE)
        draw_text_centered("On USB power", GAUGE_X,
                           int(GAUGE_VBAT_Y + ((GAUGE_H - (8*SCALE)) / 2)),
                           256, SCALE)
    else:
        BAT_THRESH = (LOW_BATTERY_VOLTAGE - VBAT_LOW) / (VBAT_HIGH - VBAT_LOW)
        bat_frac = (stats['vbat'] - VBAT_LOW) / (VBAT_HIGH - VBAT_LOW)
        bat_frac = min(1.0, max(0.0, bat_frac))
        # Overdraw hides the right border of the red segment
        w = int(bat_frac * 256)  # int(min(BAT_THRESH, bat_frac) * 256)
        draw_3d_rect(GAUGE_X, GAUGE_VBAT_Y, w, GAUGE_H,
                     WPAL_YELLOW, WPAL_RED, WPAL_DRED)
        if bat_frac > BAT_THRESH:
            w = int(bat_frac * 256) - int(BAT_THRESH * 256)
            draw_3d_rect(GAUGE_X + int(BAT_THRESH * 256), GAUGE_VBAT_Y, w, GAUGE_H,
                         WPAL_GREEN, WPAL_DGREEN, WPAL_DGREY)
            # Patch the left edge of the green segment
            display.set_pen(WPAL_DGREEN)
            display.rectangle(GAUGE_X + int(BAT_THRESH * 256), GAUGE_VBAT_Y + 2,
                              min(2, w), GAUGE_H - 4)
        display.set_pen(WPAL_WHITE)
        draw_text_centered(f"{bat_frac * 100.0:.2f}%",
                           GAUGE_X,
                           int(GAUGE_VBAT_Y + ((GAUGE_H - (8*SCALE)) / 2)),
                           256, SCALE)
        y = GAUGE_VBAT_Y + GAUGE_H - (2 + 8*2)
        display.text(f"{stats['vbat_low']:.2f}v",
                     GAUGE_X + 2, y, 252, SCALE)
        draw_text_centered(f"{stats['vbat']:.2f}v",
                           GAUGE_X + 2, y, 252, SCALE)
        draw_text_right(f"{stats['vbat_high']:.2f}v",
                        GAUGE_X + 2, y, 252, SCALE)

    w = int(stats['lum'] / (8192 / 256))  # Reduced range from 65536
    w = min(w, 256)
    draw_3d_rect(GAUGE_X, GAUGE_LUX_Y, w, GAUGE_H,
                 WPAL_WHITE, WPAL_YELLOW, WPAL_DYELLOW)
    display.set_pen(WPAL_MAGENTA)
    draw_text_centered(f"{stats['lum'] / 655.36:.2f}%",
                       GAUGE_X,
                       int(GAUGE_LUX_Y + ((GAUGE_H - (8*SCALE)) / 2)),
                       256, SCALE)
    y = GAUGE_LUX_Y + GAUGE_H - (2 + 8*2)
    display.text(f"{stats['lum_low'] / 655.36:.2f}%",
                 GAUGE_X + 2, y, 252, SCALE)
    draw_text_right(f"{stats['lum_high'] / 655.36:.2f}%",
                    GAUGE_X + 2, y, 252, SCALE)

    w = int(stats['backlight'] * 256)
    draw_3d_rect(GAUGE_X, GAUGE_BACKLIGHT_Y, w, GAUGE_H,
                 WPAL_CYAN, WPAL_DCYAN, WPAL_DBLUE)
    display.set_pen(WPAL_YELLOW)
    draw_text_centered(f"{int(stats['backlight'] * 100)}%", GAUGE_X,
                       int(GAUGE_BACKLIGHT_Y + ((GAUGE_H - (8*SCALE)) / 2)),
                       256, SCALE)

    display.update()

def hightext():
    global XSCROLL
    XSCROLL -= 10
    if XSCROLL < -(message_width + 10 + 10):
        XSCROLL = 320
    
    # for each character we'll calculate a position and colour, then draw it
    for i in range(0, len(message)):
        cx = int(XSCROLL + (i * text_size * 5.5))
#        cy = int(80 + math.sin(t * 10 + i) * 20)
        
        # to speed things up we only bother doing the hardware if the character will be visible on screen
        if cx > 10 and cx < 300:
            
            # generate a rainbow colour that cycles with time
            r, g, b = hsv_to_rgb(i / 10 + t / 5, 1, 1)        
            display.set_pen(display.create_pen(r, g, b))
            display.text(message[i], cx, 15, -1, text_size)

def set_backlight(bl):
    display.set_backlight(bl)
    
def measure_texte(at, tz):
    display.measure_text(at, tz)
    
def create_pen(zz, ee, rr):
    display.create_pen(zz, ee, rr)
    
def grid():
    grid_size = 40
    for y in range(0, 240 / grid_size):
        for x in range(0, 320 / grid_size):
            h = x + y + int(t * 5)
            h = h / 50.0
            r, g, b = hsv_to_rgb(h, .5, 1)   
            display.set_pen(display.create_pen(r, g, b))
            display.rectangle(x * grid_size, y * grid_size, grid_size, grid_size)
            
def text(text, x, y, pen, s):
    display.set_pen(pen)
    display.text(text, x, y, -1, s)
            
def listapp(applications, scroll_position, selected_item):
    for list_index, application in enumerate(applications):
        distance = list_index - scroll_position
        text_size = 4 if selected_item == list_index else 3

        # center text horixontally
        title_width = display.measure_text(application["title"], text_size)
        text_x = int(160 - title_width / 2)
        
        row_height = text_size * 5 + 20
        
        # center list items vertically
        text_y = int(120 + distance * row_height - (row_height / 2))
        
        # draw the text, selected item brightest and with shadow
        if selected_item == list_index:
          text(application["title"], text_x + 1, text_y + 1, shadow_pen, text_size)
          
        text_pen = selected_pen if selected_item == list_index else unselected_pen
        text(application["title"], text_x, text_y, text_pen, text_size)
            
