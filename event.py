from pimoroni import Button
from machine import ADC, Pin


button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
lux_vref_pwr = Pin(27, Pin.OUT)
lux = ADC(26)
led = Pin(25, Pin.OUT)
