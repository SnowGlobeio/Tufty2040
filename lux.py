# Automatic brightness example.
import time
from machine import ADC, Pin
import micropython

# Constants for automatic brightness adjustment.
# Below about 3/8ths, the backlight is entirely off. The top of the range is OK.
BACKLIGHT_LOW = micropython.const(0.375)
BACKLIGHT_HIGH = micropython.const(1.0)

# The luminance sensor seems to cover the whole 16-bit range pretty well from
# buried in shadow to bright phone torch in its face, but setting a lower high
# point will make it generally bias brighter in calm room lighting, and a higher
# low will use the darkest backlight without needing to completely hard-mask the
# sensor in complete darkness.
LUMINANCE_LOW = micropython.const(384)
LUMINANCE_HIGH = micropython.const(2048)  # 65535 to use the full range.

# If on battery, and the supply voltage drops below this, force minimum
# backlight brightness.
# The bottom of the Tufty2040 input range is 3.0v, so values below that likely
# will not trigger before it cuts out.
LOW_BATTERY_VOLTAGE = micropython.const(3.1)

lux_vref_pwr = Pin(27, Pin.OUT)
lux = ADC(26)
vbat_adc = ADC(29)
vref_adc = ADC(28)
usb_power = Pin(24, Pin.IN)

# Returns a tuple of the raw luminance value, and the brightness to now use.
def auto_brightness(previous: float) -> (float, float):
    luminance = lux.read_u16()
    luminance_frac = max(0.0, float(luminance - LUMINANCE_LOW))
    luminance_frac = min(1.0, luminance_frac / (LUMINANCE_HIGH - LUMINANCE_LOW))
    backlight = BACKLIGHT_LOW + (luminance_frac * (BACKLIGHT_HIGH - BACKLIGHT_LOW))
    # Use the previous value to smooth out changes to reduce flickering.
    # The "32" value here controls how quickly it reacts (larger = slower).
    # The rate at which the main loop calls us also affects that!
    backlight_diff = backlight - previous
    backlight = previous + (backlight_diff * (1.0 / 32.0))
    return (luminance, backlight)


# Returns a tuple of voltage (fake value if on USB), "is on USB", and "is low".
def measure_battery() -> (float, bool, bool):
    if usb_power.value():
        return (5.0, True, False)

    # See the battery.py example for how this works.
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = ((vbat_adc.read_u16() / 65535) * 3 * vdd)

    low_battery = False
    if vbat < LOW_BATTERY_VOLTAGE:
        low_battery = True
    return (vbat, False, low_battery)

