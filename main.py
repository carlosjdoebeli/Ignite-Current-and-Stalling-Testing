"""
Created on 19 February 2019
@author: Carlos Doebeli

Switch must initially be off before the test begins, or the code will not work.
This is a code for an Adafruit Metro M4 Microcontroller. The circuit should be connected to a force load cell,
a circuit sensor, and a switch.
"""


import board
import busio
import digitalio
from analogio import AnalogIn
from pni_libs.helpers import chronometer
from pni_libs.debug import *
from pni_libs.rs485 import *


class StallingCurrent:

    def __init__(self):
        Debug.begin(debug_level=Debug.DEBUG)
        self.force_sensor = AnalogIn(board.A2)
        self.current_sensor = AnalogIn(board.A3)
        self.switch = digitalio.DigitalInOut(board.D10)
        self.switch.direction = digitalio.Direction.INPUT
        self.switch.pull = digitalio.Pull.UP
        self.running = False

        self.force_times = []
        self.force_data = []
        self.current_times = []
        self.current_data = []
        self.start_time = millis()

        self.chrono = chronometer()
        self.chrono_time = 1                        # THIS IS THE DELAY THAT CAN BE CHANGED AND CONFIGURED
        self.chrono.set(self.chrono_time)
        self.chrono.start()

    def loop(self):
        if not self.switch.value and not self.running:
            self.start()

        if self.running and self.switch.value:
            self.end()

        # if self.running:      # FOR THE HIGHEST RESOLUTION WITH NO DELAYS, UNCOMMENT THIS LINE
        if self.running and self.chrono.isDone():       # FOR NO DELAYS, COMMENT THIS LINE OUT
            force_voltage = ((self.force_sensor.value - 250) * self.force_sensor.reference_voltage) / 65535
            force_lbs = (force_voltage - 0.0438) * 500.0000 / (0.1000 * 33.0000)
            self.force_times.append((millis() - self.start_time) / 1000.0000)
            self.force_data.append(force_lbs)

            current_voltage = ((self.current_sensor.value - 362) * self.current_sensor.reference_voltage) / 65535
            current_amps = (current_voltage - 2.4858) * 5.6500
            self.current_times.append((millis() - self.start_time) / 1000.0000)
            self.current_data.append(current_amps)

            # Debug messages to determine the force voltage and force output, as well as current voltage and current output
            # If the output force is not 0, then use these to determine how to recalibrate and change the above lines.

            # Debug.msg("{0} volts, {1} lbs".format(force_voltage, force_lbs), Debug.DATA, source="Force Sensor")
            # Debug.msg("{0} volts, {1} amps".format(current_voltage, current_amps), Debug.DATA, source="Current Sensor")

            self.chrono.setAndGo(self.chrono_time)      # Comment this out for higher resolution

    def initialize(self):
        if self.switch.value:
            self.start()

    def start(self):
        self.running = True
        self.force_times = []
        self.force_data = []
        self.current_times = []
        self.current_data = []
        self.start_time = millis()
        print("Starting")

    def end(self):
        self.running = False
        print("Start of Test")

        print("Force Data")
        for i in range(0, len(self.force_data)):
            print("{0}, {1}".format(self.force_times[i], self.force_data[i]))
        print("End Force Data")

        print("Current Data")
        for i in range(0, len(self.current_data)):
            print("{0}, {1}".format(self.current_times[i], self.current_data[i]))
        print("End Current Data")

        print("End of Test\n\n")


if __name__ == "__main__":
    neopixel_off()
    app = StallingCurrent()
    app.initialize()
    print("MCU Ready")
    app.initialize()
    while True:
        try:
            app.loop()
        except MemoryError:
            print("Error allocating memory.")
            app.end()
