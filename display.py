# This code shows main information of raspberry pi system on a display

import math
import Adafruit_SSD1306 as SSD

from PIL import Image, ImageDraw, ImageFont

import common


class CpuLoadTile():

    # Constants
    __RADIUS = 15
    __INK = 255
    __INK_BKG = 0
    __WIDTH = 1

    def __init__(self, center: tuple[float, float], draw: ImageDraw, font: ImageFont):
        self.__center = center
        self.__draw = draw
        self.__font = font

        self.__textLocation = (self.__center[0] * 0.1, self.__center[1] + 1)
        self.__value = -1.0
        self.__line = [0, 0, 0, 0]
        self.__text = ''

        self.__drawArc()

    def updateValue(self, cpuLoad: float) -> None:
        if cpuLoad != self.__value:
            self.__value = cpuLoad
            angle = 1.8 * cpuLoad

            # Remove privious arrow and redraw arc line
            self.__draw.line(self.__line, self.__INK_BKG, self.__WIDTH)
            self.__drawArcLine()

            # Draw new arrow
            arrowEnd = self.__getArrowEnd(angle)
            self.__line = [self.__center[0], self.__center[1], arrowEnd[0], arrowEnd[1]]
            self.__draw.line(self.__line, self.__INK, self.__WIDTH)

            # Remove privious text and draw a new one
            self.__draw.text(self.__textLocation, self.__text, self.__INK_BKG, self.__font)
            self.__text = f'{cpuLoad}%'
            self.__draw.text(self.__textLocation, self.__text, self.__INK, self.__font)

    def __getArrowEnd(self, angle: float) -> tuple[float, float]:
        angle *= math.pi / 180
        x = self.__center[0] - self.__RADIUS * 0.85 * math.cos(angle)
        y = self.__center[1] - self.__RADIUS * 0.85 * math.sin(angle)
        return (x, y)
    
    def __drawArc(self) -> None:
        arcBox = [self.__center[0] - self.__RADIUS, self.__center[1] - self.__RADIUS, self.__center[0] + self.__RADIUS, self.__center[1] + self.__RADIUS]
        self.__draw.arc(arcBox, 180, 0, self.__INK, self.__WIDTH)
        self.__drawArcLine()

    def __drawArcLine(self) -> None:
        self.__draw.line([self.__center[0] - self.__RADIUS, self.__center[1], self.__center[0] + self.__RADIUS, self.__center[1]], self.__INK, self.__WIDTH)

class CpuTemperatureTile():

    # Constants
    __RADIUS = 15
    __INK = 255
    __INK_BKG = 0
    __WIDTH = 1

    def __init__(self, center: tuple[float, float], draw: ImageDraw, font: ImageFont):
        self.__center = center
        self.__draw = draw
        self.__font = font

        self.__textLocation = (self.__center[0] * 0.1, self.__center[1])
        self.__value = -1.0
        self.__line = [0, 0, 0, 0]
        self.__text = ''

        self.__drawArc()

    def updateValue(self, cpuTemp: float) -> None:
        if cpuTemp != self.__value:
            self.__value = cpuTemp
            angle = 1.8 * cpuTemp

            # Remove privious arrow and redraw arc line
            self.__draw.line(self.__line, self.__INK_BKG, self.__WIDTH)
            self.__drawArcLine()

            # Draw new arrow
            arrowEnd = self.__getArrowEnd(angle)
            self.__line = [self.__center[0], self.__center[1] + self.__RADIUS, arrowEnd[0], arrowEnd[1] + self.__RADIUS]
            self.__draw.line(self.__line, self.__INK, self.__WIDTH)

            # Remove privious text and draw a new one
            self.__draw.text(self.__textLocation, self.__text, self.__INK_BKG, self.__font)
            self.__text = f'{cpuTemp}\'C'
            self.__draw.text(self.__textLocation, self.__text, self.__INK, self.__font)

    def __getArrowEnd(self, angle: float) -> tuple[float, float]:
        angle *= math.pi / 180
        x = self.__center[0] + self.__RADIUS * 0.85 * math.cos(angle)
        y = self.__center[1] + self.__RADIUS * 0.85 * math.sin(angle)
        return (x, y)

    def __drawArc(self) -> None:
        arcBox = [self.__center[0] - self.__RADIUS, self.__center[1], self.__center[0] + self.__RADIUS, self.__center[1] + self.__RADIUS * 2]
        self.__draw.arc(arcBox, 0, 180, self.__INK, self.__WIDTH)
        self.__drawArcLine()

    def __drawArcLine(self) -> None:
        self.__draw.line([self.__center[0] - self.__RADIUS, self.__center[1] + self.__RADIUS, self.__center[0] + self.__RADIUS, self.__center[1] + self.__RADIUS], self.__INK, self.__WIDTH)

class IpTile():

    # Constants
    __INK = 0
    __INK_BKG = 128
    
    def __init__(self, location: tuple[float, float], draw: ImageDraw, font: ImageFont, fontSize: float, displayWidth: float):
        self.__location = location
        self.__draw = draw
        self.__font = font

        self.__width = displayWidth - location[0]
        self.__height = fontSize + 2
        self.__textLocation = [location[0] + self.__height + 5, location[1] - 1]
        self.__text = ''

        self.__drawBackground()

    def updateValue(self, ip: str) -> None:
        if self.__text != ip:
            self.__draw.text(self.__textLocation, self.__text, self.__INK_BKG, self.__font)
            self.__text = ip
            self.__draw.text(self.__textLocation, self.__text, self.__INK, self.__font)

    def __drawBackground(self) -> None:
        # Draw rectangle
        rect = [self.__location[0], self.__location[1], self.__location[0] + self.__width, self.__location[1] + self.__height]
        self.__draw.rectangle(rect, fill=self.__INK_BKG)
        # Remove arc part from it
        arcBox = [self.__location[0] - self.__height, self.__location[1], self.__location[0] + self.__height, self.__location[1] + self.__height * 2]
        self.__draw.arc(arcBox, 270, 0, self.__INK, self.__height + 1)

class BarTile():

    # Constants
    __INK = 255
    __INK_BKG = 0

    def __init__(self, location: tuple[float, float], draw: ImageDraw, font: ImageFont, fontSize: float, displayWidth: float, name: str, maxValue: float, unit: str):
        self.__location = location
        self.__draw = draw
        self.__font = font
        self.__name = name
        self.__maxValue = maxValue
        self.__unit = unit

        self.__barLocation = [location[0], location[1] + fontSize + 3]
        self.__barWidth = displayWidth - location[0]
        self.__barHeight = fontSize / 2
        self.__value = -1.0
        self.__rectFill = [0, 0, 0, 0]
        self.__text = ''

        self.__drawBar()

    def updateValue(self, actual: float) -> None:
        if actual != self.__value:
            self.__value = actual
            # Redraw text
            self.__draw.text(self.__location, self.__text, self.__INK_BKG, self.__font)
            self.__text = f'{self.__name}: {actual}/{self.__maxValue} {self.__unit}'
            self.__draw.text(self.__location, self.__text, self.__INK, self.__font)

            # Redraw bar
            self.__draw.rectangle(self.__rectFill, self.__INK_BKG, 0)
            percentage = actual / self.__maxValue
            self.__rectFill = [self.__barLocation[0] + 1, self.__barLocation[1] + 1, self.__barLocation[0] + 1 + (self.__barWidth - 3) * percentage, self.__barLocation[1] + self.__barHeight - 1]
            self.__draw.rectangle(self.__rectFill, self.__INK, 0)

    def __drawBar(self) -> None:
        rect = [self.__barLocation[0], self.__barLocation[1], self.__barLocation[0] + self.__barWidth - 1, self.__barLocation[1] + self.__barHeight]
        self.__draw.rectangle(rect, self.__INK_BKG, self.__INK, 1)

class DashBoard():

    # Constants
    __RST = None        # On the PiOLED this pin isnt used
    __FONT_SIZE = 10    # Font size

    def __init__(self, gpio):
        self.__disp = SSD.SSD1306_128_64(rst=self.__RST, gpio=gpio)                        # 128x64 display with hardware I2C
        self.__image = Image.new('1', (self.__disp.width, self.__disp.height))  # Create blank image for drawing. Make sure to create image with mode '1' for 1-bit color.
        self.__draw = ImageDraw.Draw(self.__image)                              # Get drawing object to draw on image.
        self.__font = ImageFont.truetype('SoletoTK.ttf', self.__FONT_SIZE)      # Define a new true type font for drawing text

        self.__disp.begin()     # Initialize display library
        self.__disp.clear()     # Clear display
        self.__disp.display()   # Invalidate display

        self.__initializeTiles()
        self.__updateDisplay()

    def updateDashboard(self, cpuLoad: float, cpuTemp: float, ip: str, ram: float, sd: float, usb: float) -> None:
        self.__ipTile.updateValue(ip)
        self.__cpuLoadTile.updateValue(cpuLoad)
        self.__cpuTempTile.updateValue(cpuTemp)
        self.__barRamTile.updateValue(ram)
        self.__barSdTile.updateValue(sd)
        self.__barUsbTile.updateValue(usb)

        self.__updateDisplay()

    def clear(self) -> None:
        self.__draw.rectangle([0, 0, self.__disp.width, self.__disp.height])

    def __initializeTiles(self) -> None:
        self.__ipTile = IpTile([25, 0], self.__draw, self.__font, self.__FONT_SIZE, self.__disp.width)
        self.__cpuLoadTile = CpuLoadTile([15, 19], self.__draw, self.__font)
        self.__cpuTempTile = CpuTemperatureTile([15, 30], self.__draw, self.__font)
        self.__barRamTile = BarTile([37, 11], self.__draw, self.__font, self.__FONT_SIZE, self.__disp.width, 'RAM', common.getTotalRam(), 'Gi')
        self.__barSdTile = BarTile([37, 28], self.__draw, self.__font, self.__FONT_SIZE, self.__disp.width, 'SD', common.getTotalSd(), 'Gi')
        self.__barUsbTile = BarTile([37, 45], self.__draw, self.__font, self.__FONT_SIZE, self.__disp.width, 'USB', common.getTotalUsb(), 'Gi')

    def __updateDisplay(self) -> None:
        self.__disp.image(self.__image) # Draw image into display
        self.__disp.display()           # Invalidate display