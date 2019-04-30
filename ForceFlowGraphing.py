"""
Created on Friday, April 26, 2019
@author: Carlos Doebeli

This is a simple script to overlay force data and flow data to create several graphs with force overlaid with flow rate.

This code was created with the assumption that the data was created with the StallingCurrentMonitor or ForceMonitor
scripts, as well as the Flow Plot software. The code assumes that there is one flow rate plot for each force plot, each
with the same naming conventions.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import os
import sys
import time

force_files = []
flow_files = []
path = sys.path[0]   # Configure this path each time you use the code
force_file_names = []
flow_file_names = []
force_labels = []
flow_labels = []

force_times = []
forces = []
flow_times = []
flow_rates = []


# This depends on the names of the files containing your force and flow data!
# This assumes they are in subdirectories of the script's directory, called Force Data and Flow Data. 
def openFiles():
    for fileName in os.listdir(path + "/Force Data"):
        if fileName.endswith(".txt"):
            force_file_names.append(fileName)
            force_filePath = path + "/Force Data/" + fileName
            f = open(force_filePath, "r")
            force_files.append(f)

    for fileName in os.listdir(path + "/Flow Data"):
        if fileName.endswith(".txt"):
            flow_file_names.append(fileName)
            flow_filePath = path + "/Flow Data/" + fileName
            f = open(flow_filePath, "r")
            flow_files.append(f)


def closeFiles():
    for f in force_files:
        f.close()
    for f in flow_files:
        f.close()


def plot():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H.%M', t)

    for j in range(0, len(force_files)):
        rampup_force_times = []
        rampup_forces = []
        rampup_flow_times = []
        rampup_flow_rates = []

        for k in range(0, len(force_times[j])):
            if force_times[j][k] > 5:
                break
            rampup_force_times.append(force_times[j][k])
            rampup_forces.append(forces[j][k])

        for k in range(0, len(flow_times[j])):
            if flow_times[j][k] > 5:
                break
            rampup_flow_times.append(flow_times[j][k])
            rampup_flow_rates.append(flow_rates[j][k])

        file_name = force_file_names[j].split("_")
        test_desc = "FF_" + file_name[1] + "_" + file_name[2] + "_" + file_name[3]
        title = "Force and Flow Rate Testing, " + file_name[1] + " syringe, " + file_name[2].replace("-", "/")
        fig, ax1 = plt.subplots()
        # ax1.plot(force_times[j], forces[j], 'b', label="Force")
        ax1.plot(rampup_force_times, rampup_forces, 'b', label="Force")
        ax1.set_title(title)
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('Force(lbs)', color='b')
        ax1.tick_params('y', colors='b')
        ax1bottom, ax1top = ax1.get_ylim()
        ax1.set_ylim(min(ax1bottom, -0.5), max(ax1top, 1))

        with sns.axes_style("whitegrid"):
            ax2 = ax1.twinx()
            # ax2.plot(flow_times[j], flow_rates[j], 'r', label="Flow Rate")
            ax2.plot(rampup_flow_times, rampup_flow_rates, 'r', label="Flow Rate")
            ax2.set_ylabel('Flow Rate (mL/min)', color='r')
            ax2.tick_params('y', colors='r')
            ax2bottom, ax2top = ax2.get_ylim()
            ax2.set_ylim(min(ax2bottom, -0.05), max(ax2top + 0.1, 0.25))

        graph_location = path + "/Force vs. Flow Graphs/"  # Configure your path for graphs

        if not os.path.isdir(graph_location):
            os.makedirs(graph_location)

        graph_location += test_desc + "_"
        graph_location += timestamp + ".png"
        fig.savefig(graph_location)


openFiles()

for i in range(0, len(force_files)):
    force_times.append([])
    forces.append([])
    titled = False

    for line in force_files[i]:
        data = line.split(', ')
        if len(data) == 1 and not titled:
            force_labels.append(data[0].rstrip("\n\r"))
            titled = True
        elif len(data) >= 2:
            force_times[i].append(float(data[0]))
            forces[i].append(float(data[1]))

    if not titled:
        force_labels.append("Series " + str(i + 1))

for i in range(0, len(flow_files)):
    flow_times.append([])
    flow_rates.append([])
    titled = False

    for line in flow_files[i]:
        data = line.split(';')
        if len(data) == 1 and not titled:
            flow_labels.append(data[0].rstrip("\n\r"))
            titled = True
        elif len(data) >= 2:
            flow_times[i].append(float(data[0]))
            flow_rates[i].append(float(data[1]))

    if not titled:
        flow_labels.append("Flow Rate Data")

for i in range(0, len(flow_rates)):
    force_max_time = force_times[i][len(force_times[i]) - 1]
    flow_max_time = flow_times[i][len(flow_times[i]) - 1]
    max_time_difference = force_max_time - flow_max_time

    if max_time_difference >= 0:
        for j in range(0, len(flow_times[i])):
            flow_times[i][j] += max_time_difference
    else:
        for j in range(0, len(force_times[i])):
            force_times[i][j] -= max_time_difference

    if i == 0 or i == 1 or i == 3 or i == 6:
        for j in range(0, len(flow_rates[i])):
            flow_rates[i][j] /= 10
    else:
        for j in range(0, len(flow_rates[i])):
            flow_rates[i][j] /= 5

plot()
closeFiles()
print("Success!")
