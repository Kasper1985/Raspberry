# This code configures LED lights on cpu fan and on the back of display
# depending on cpu temperature to visually indicate speed of cpu fan rotation

import time
import threading
from rpi_ws281x import PixelStrip, Color

# Constants
FREQUENCY = 800000    # LED signal frequency 800kHz
DMA = 10              # DMA channel to use for generation signal
BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
INVERT = False        # True to invert the signal (when using NPN transistor level shift)
POSITION_STEP = 85    # Color shift position step for calculation rainbow
WAIT_MS = 20          # Wait time for rainbow rotation in miliseconds

def init(count: int, pin: int) -> PixelStrip:
    """
    Initializes LED strip.
    count: count of led pixels in strip.
    pin: GPIO pin connected to the pixels.
    Returns instance of 'PixelStrip' class ready to be configured.
    """
    channel = 0
    if pin in [13, 19, 41, 45, 53]: channel = 1
    strip = PixelStrip(count, pin, FREQUENCY, DMA, INVERT, BRIGHTNESS, channel)
    strip.begin()
    return strip

def setInnerLight(strip: PixelStrip, red: int, green: int, blue: int) -> None:
    """
    Turns the light under the display on that is not on the cpu fan.
    strip: LED strip to be configured.
    red: 0-255 for red color.
    green: 0-255 for green color.
    blue: 0-255 for blue color.
    """
    strip.setPixelColor(0, Color(red, green, blue))
    strip.show()

def clear(strip: PixelStrip) -> None:
    """
    Turn the whole LED srtip off.
    strip: LED strip to be configured.
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def wheel(pos: int) -> Color:
    """
    Generate rainbow colors across 0-255 positions.
    pos: Current position for rainbow calculation.
    Returns instance of the color to be set for given position.
    """
    if pos < POSITION_STEP:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < POSITION_STEP * 2:
        pos -= POSITION_STEP
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= POSITION_STEP * 2
        return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip: PixelStrip, stop_event: threading.Event) -> None:
    """
    Draw rainbow that uniformly distributes itself across all pixels.
    strip: LED strip to be configured.
    stop_event: Threading event to be fired from the host to stop current function.
    """
    while not stop_event.is_set():
        for j in range(256):
            for i in range(1, strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(WAIT_MS / 1000.0)

            if stop_event.is_set():
                break
