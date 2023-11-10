# This is the main configuration code to setup
# cpu fan velocity depending on cpu temperature
# and adjust LED strip of the tower

import time
import threading
import RPi.GPIO as GPIO

import common
import led
from fan import CPU_FAN
from display import DashBoard

# Initialize GPIO configuration for CPU fan
FAN_CHANNEL = 8  # Default pin of fany is a physical pin 8 (GPIO14)

# Initialize GPIO and LED configuration for LED strip
LED_COUNT = 4    # Number of LED pixels
LED_PIN = 18     # GPIO pin the led strip is connected to (18 uses PWM!)

GPIO.setwarnings(False)   # disable warnings about GPIO
GPIO.setmode(GPIO.BOARD)  # set GPIO mode to BOARD

# Initialize CPU fan
fan = CPU_FAN(GPIO, FAN_CHANNEL)

# Initialize LED strip and working deamon
strip = led.init(LED_COUNT, LED_PIN)
stop_event = threading.Event()
ledThread = threading.Thread(target=led.rainbowCycle, args=(strip, stop_event))
ledThread.daemon = True

# Initialize display dashboard
dashBoard = DashBoard(GPIO)

try:
    while True:
        # Setup cpu fan
        temp = common.getCpuTemperature()
        isFanOn = fan.setCpuFanSpeed(temp)

        # Setup led strip
        if isFanOn and not ledThread.is_alive():
            stop_event.clear()
            ledThread.start()
        elif not isFanOn and ledThread.is_alive():
            stop_event.set()
            led.clear(strip)

        # Setup display
        cpuLoad = common.getCpuLoad()
        cpuTemp = common.getCpuTemperature()
        ip = common.getIP()
        ram = common.getUsedRam()
        sd = common.getUsedSd()
        usb = common.getUsedUsb()
        dashBoard.updateDashboard(cpuLoad, cpuTemp, ip, ram, sd, usb)

        time.sleep(1)

except KeyboardInterrupt:
    pass

stop_event.set()    # stop led thread
led.clear(strip)    # turn off all led pixels
fan.clear()         # stop cpu fan
dashBoard.clear()   # clear display
#GPIO.cleanup()     # clean up GPIO board