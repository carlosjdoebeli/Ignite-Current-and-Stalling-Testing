# Ignite-Current-and-Stalling-Testing

This is the repository for tests involving measurements of force and current with an Adafruit Metro M4. This script should be used in conjunction with the already-built microcontroller circuit with a load cell and circuit sensor. 

## Instructions of Use
An Adafruit Metro M4 must be connected to your computer. The files in the "Metro M4" subdirectory should be copied onto the Metro M4.

Depending on the application, either the <b>StallingCurrentMonitor.py</b> or <b>ForceMonitor.py</b> can be used to gather the data, put 
it into files, and graph the data. The ForceFlowGraphing file is used to combine force data with flow plot data created with a flowmeter 
and graph them on the same plot. 

Run the relevant script from the command line. There should only be one COM Port that registers as a "USB Serial Device", 
otherwise the code will not run. If you have more than one USB Serial Device connected to your computer, either remove the other USB 
Serial Device connections, or alter the code to input the COM Port and baudrate manually. 

Ensure that the load cell and current sensor are connected to the appropriate places on the microcontroller's attached breadboard. Ensure that the switch connected to the microcontroller is OFF to start the test. 

Input a test description for the heating test that you are running, such as <b>"CS_Inst6_500RPM_25C_128MS_Motor1_1"</b>. Here, CS is the abbreviation of the test you are conducting. Inst6, 500RPM, 25C, and 128MS refer to the instrument and its speed, current driver, and microstepping settings.

Turn on the switch when you want to start taking data. Turn the switch off when you wish to end the test. 

The script will create data files for force and current measurements, as well as one graph overlaying the data from the sensors used onto one graph. From the root directory, the data files will be located in the folder:

<b>rootdir/Data/test_desc.txt</b>

The graph will be located in the folder:

<b>rootdir/Graphs/test_desc.png</b>

Where rootdir is the directory the script is being run from, and test_desc is the inputted test description including the time stamp. Note that for data files, whether the data is Force or Current data will also be included in the file name. The previous example would produce a data file with a name:

<b>"CS_Inst6_500RPM_25C_128MS_Motor1_Current_Feb-21-2019_10.08"</b>

And another one for force. The graph will have a similar name. The data files will have Force or Current appended to the file name, and the created files will have a timestamp in the file name. 

There are some commented-out print statements. For debugging, these may be useful when uncommented. Further information on the test can be seen at https://docs.google.com/document/d/1CGmDpNfZzwRRA_P1ybclhYgYVG9C83D-rd2c-g5TQj8/edit. 
