# This code automatically adjusts cpu fan speed depending on the cpu temperature.

class CPU_FAN:

    # Constants
    __FREQUENCY = 50          # modulation frequency 50Hz
    __TEMP_LEVEL_LOW = 45     # low temerature level
    __TEMP_LEVEL_MID = 55     # middle temperature level
    __TEMP_LEVEL_HIGH = 65    # high temperature level
    __TEMP_TRESHOLD = 5       # temperature treshold for shutting down the cpu fan
    __DUTY_CYCLE_NONE = 0     # duty cycle at 0%
    __DUTY_CYCLE_LOW = 80     # duty cycle at 80%
    __DUTY_CYCLE_MID = 90     # duty cycle at 90%
    __DUTY_CYCLE_HIGH = 100   # duty cycle at 100%

    def __init__(self, GPIO, channel: int):
        """
        Initializes cpu fan GPIO to control fan speed.
        GPIO: GPIO configuration for the board.
        channel: power out pin for cpu fan.
        """
        GPIO.setup(channel, GPIO.OUT)                       # setup fan pin as an output connection
        self.__pwm = GPIO.PWM(channel, self.__FREQUENCY)    # set frequency for power with modulation
        self.__dutyCycle = self.__DUTY_CYCLE_NONE           # initialize starting duty cycle of the fan
        self.__pwm.start(self.__dutyCycle)                  # start modulation with duty cycle 0

    def setCpuFanSpeed(self, temp: float) -> bool:
        """
        Sets the cpu fan speed accordingly to cpu temperature.
        temp: actual cpu temperature.
        Returns state if the cpu fan was turned on.
        """
        neededDutyCycle = self.__getDutyCycleByTemp(temp)
        if self.__dutyCycle != self.__DUTY_CYCLE_NONE:
            if self.__dutyCycle < neededDutyCycle:
                self.__dutyCycle = neededDutyCycle
            elif temp <= (self.__TEMP_LEVEL_LOW - self.__TEMP_TRESHOLD):
                self.__dutyCycle = self.__DUTY_CYCLE_NONE
        else:
            self.__dutyCycle = neededDutyCycle

        self.__pwm.ChangeDutyCycle(self.__dutyCycle)
        return self.__dutyCycle != self.__DUTY_CYCLE_NONE

    def clear(self) -> None:
        """Stops the pulse width modulation for cpu fan pin."""
        self.__pwm.stop()

    def __getDutyCycleByTemp(self, temperature: int) -> int:
        """
        Defines the duty cycle by cpu temperature.
        temperature: actual temperature of the cpu.
        Returns needed duty cycle to control fan speed.
        """
        dutyCycle = self.__DUTY_CYCLE_NONE
        if temperature >= self.__TEMP_LEVEL_LOW:  dutyCycle = self.__DUTY_CYCLE_LOW
        if temperature >= self.__TEMP_LEVEL_MID:  dutyCycle = self.__DUTY_CYCLE_MID
        if temperature >= self.__TEMP_LEVEL_HIGH: dutyCycle = self.__DUTY_CYCLE_HIGH
        return dutyCycle