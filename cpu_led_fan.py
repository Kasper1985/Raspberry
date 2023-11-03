import RPi.GPIO as GPIO
import time
import subprocess as sp

# initialize GPIO configuration for CPU fan
# Default pin of fan is physical pin 8 (GPIO 14)
FAN_CHANNEL = 8

GPIO.setmode(GPIO.BOARD)          # set GPIO mode to BOARD
GPIO.setup(FAN_CHANNEL, GPIO.OUT) # setup pin 8 as output connection

p = GPIO.PWM(FAN_CHANNEL, 50) # setup a power width modulation for channel 8 with frequency of 50Hz
p.start(0)                    # start modulation with duty cycle 0


command = ''
while command != 'q':
    # ask for the duty cycle
    command = input("Enter a new duty cycle or 'q' to quit: ")

    # check input parameters
    try:
        dutyCycle = int(command)
        if dutyCycle < 0: dutyCycle = 0
        elif dutyCycle > 100: dutyCycle = 100
    except ValueError:
        dutyCycle = 0
        pass
    
    p.ChangeDutyCycle(dutyCycle)

# Before quiting the programm cleanup the GPIO
p.ChangeDutyCycle(0)
p.stop()
#GPIO.cleanup()