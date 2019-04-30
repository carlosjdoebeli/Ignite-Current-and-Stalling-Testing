"""
Created on 19 February 2019
@author: Carlos Doebeli

Switch must initially be off before the test begins, or the code will not work.
"""

import numpy as np
from numpy import diff
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import re
import time
import serial
import serial.tools.list_ports
import os
import sys


# Which port you connect to will depend on your computer's connections
ports = list(serial.tools.list_ports.grep("USB Serial Device"))
force_times = []
force_data = []
current_times = []
current_data = []

if len(ports) == 1:
    print("USB Serial Device found")
else:
    print("USB Serial Device not found or too many of them.")
    print("Check your connections!")
    time.sleep(1)
    sys.exit()

serial_port = ports[0]
print(serial_port)
ser = serial.Serial(serial_port[0], 9600)

file_path = sys.path[0]

if not os.path.isdir(file_path + "/Data/"):
    os.makedirs(file_path + "/Data/")
if not os.path.isdir(file_path + "/Graphs/"):
    os.makedirs(file_path + "/Graphs/")


def read_forces():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H.%M', t)
    file_name = file_path + "/Data/"
    file_name += test_desc + "_Force_" + timestamp + ".txt"
    f = open(file_name, "w+")

    line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
    if "Force Data" in line:
        while "End" not in line:
            f.write(line + "\n")
            line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
            # force_line = re.findall('-?\d+\.?\d*', line)
            force_line = line.split(", ")
            if len(force_line) >= 2:
                force_times.append(float(force_line[0]))
                force_data.append(float(force_line[1]))

    f.close()
    max_force = max(force_data)
    print("Maximum force is {0}".format(max_force))


def plot():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H.%M', t)

    fig, ax1 = plt.subplots()
    ax1.plot(force_times, force_data, 'b', label="Force")
    ax1.set_title(test_desc)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Force (lbs)', color='b')
    ax1.tick_params('y', colors='b')
    ax1bottom, ax1top = ax1.get_ylim()
    ax1.set_ylim(min(ax1bottom, -0.5), max(ax1top, 5))

    file_name = file_path + "/Graphs/"  # Configure your path for graphs

    if not os.path.isdir(file_name):
        os.makedirs(file_name)

    file_name += test_desc + "_"
    file_name += timestamp + ".png"
    fig.savefig(file_name)
    plt.show()


test_desc = input("Please enter test description: ")
print("Turn on the switch to take data.")

while True:
    line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
    if "Starting" in line:
        print(line)
    if "Error" in line:
        print(line)
    if "Start of Test" in line:
        print("Compiling results...")
        break

read_forces()
plot()
ser.close()
