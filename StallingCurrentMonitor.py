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
import os

# Which port you connect to will depend on your computer's connections
ser = serial.Serial('COM24', 9600)  # Establish the connection on a specific port
force_times = []
force_data = []
current_times = []
current_data = []
filePath = "C:/Users/cdoebeli/Google Drive/2.0 Engineering Projects/Ignite Project/6.0 Testing/Ignite Current and Stalling/" #Configure your path for data
if not os.path.isdir(filePath):
    os.makedirs(filePath)
if not os.path.isdir(filePath + "Data/"):
    os.makedirs(filePath + "Data/")
if not os.path.isdir(filePath + "Graphs/"):
    os.makedirs(filePath + "Graphs/")


def read_forces():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H.%M', t)
    fileName = filePath + "Data/"
    fileName += test_desc + "_Force_" + timestamp + ".txt"
    f = open(fileName, "w+")

    line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
    if "Force Data" in line:
        while "End" not in line:
            f.write(line + "\n")
            line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
            force_line = re.findall('-?\d+\.?\d*', line)
            if len(force_line) >= 2:
                force_times.append(float(force_line[0]))
                force_data.append(float(force_line[1]))


def read_currents():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H.%M', t)
    fileName = filePath + "Data/" + test_desc + "_Current_" + timestamp + ".txt"
    f = open(fileName, "w+")

    line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
    if "Current Data" in line:
        while "End" not in line:
            f.write(line + "\n")
            line = str(ser.readline()).replace("b'", "").replace(r"\r\n'", "")
            current_line = re.findall('-?\d+\.?\d*', line)
            # current_line = line.split(", ")
            if len(current_line) >= 2:
                current_times.append(float(current_line[0]))
                current_data.append(float(current_line[1]))


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

    with sns.axes_style("whitegrid"):
        ax2 = ax1.twinx()
        ax2.plot(current_times, current_data, 'r', label="Current")
        ax2.set_ylabel('Current (A)', color='r')
        ax2.tick_params('y', colors='r')
        ax2bottom, ax2top = ax2.get_ylim()
        ax2.set_ylim(min(ax2bottom, -0.05), max(ax2top + 0.1, 0.25))

    # fig.tight_layout()

    fileName = filePath + "Graphs/"  # Configure your path for graphs

    if not os.path.isdir(fileName):
        os.makedirs(fileName)

    fileName += test_desc + "_"
    fileName += timestamp + ".png"
    fig.savefig(fileName)
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
read_currents()
plot()
ser.close()
