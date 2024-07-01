# Python code to interface with the RADbox model. Plots data in real time and saves it to a CSV file

import sys
import subprocess
import serial
import serial.tools.list_ports
import csv
import time
from datetime import datetime

# The plotting stuff is a wee bit jank, so there is some code there that ignores an error message that doesn't matter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import backend_bases
if not sys.warnoptions:
    import warnings
    warnings.filterwarnings("ignore") 
plt.rcParams['toolbar'] = 'toolmanager'

import seaborn as sns


# Arduino raw inputs; try/except clause because I kept forgetting to plug it in
# This reads for the SEEED board exclusively
try:
    # Automatically detects the arduino port
    ports = list(serial.tools.list_ports.comports())
    for devi in ports:
        if "CP2102N" in devi.description:
            arduino_port = devi.device

    baud = 115200
    serial_connection = serial.Serial(arduino_port, baud)
except:
    print("Please plug in the arduino.")
    sys.exit()

# Set up CSV; name is given with time so that multiple runs can be done consecutively. File name involves a different unicode character that looks like a colon (but isn't), to avoid windows issues
not_colon = "\ua789"
csv_file = datetime.now().strftime(f"raw-data-%Y-%m-%d-%H{not_colon}%M{not_colon}%S.csv")
file = open(csv_file, "a")

# Getting user input and reading that many samples
user_input = input("How many samples would you like to take? 12 scans takes roughly 1 minute.\n")

# This try/except clause checks to see if the user input an integer
try:
    number_of_samples = int(user_input)
except:
    print("Please input an integer (e.g. 1, 2, 3...)")
    exit()
else:
    # Estimates how long it will take
    sampling_time = (number_of_samples * 5)/60  # takes one sample every 5 secs
    print(
        f"It will take roughly {round(sampling_time, 2)} minute(s) to collect the data."
        )

time_data = []
co2_raw_data = []
voc_raw_data = []
nox_raw_data = []
temp_raw_data = []
humi_raw_data = []
x_axis_max = (number_of_samples * 7)

# Plotting stuff
sns.set_style("ticks")

# axes in same order as empty lists
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1) 
# plt.xlim(0, x_axis_max)

fig.suptitle("Air Quality Levels Over Time", fontsize=16)

# only need to label the one because they share the same axis
ax5.set_xlabel("Time (s)", fontsize=14)

ax1.set_ylabel(r"CO$_2$ (ppm)")
ax2.set_ylabel("VOC (ppb)")
ax3.set_ylabel(r"NO$_x$  (ppb)")
ax4.set_ylabel(r"Temp ($^o$C)")
ax5.set_ylabel("Humi (%RH)")

ax1.set_xlim([0, x_axis_max])
ax2.set_xlim([0, x_axis_max])
ax3.set_xlim([0, x_axis_max])
ax4.set_xlim([0, x_axis_max])
ax5.set_xlim([0, x_axis_max])

# The plots
ln1, = ax1.plot(time_data, co2_raw_data, '-o', color="blue")
ln2, = ax2.plot(time_data, voc_raw_data, '-v', color="black")
ln3, = ax3.plot(time_data, nox_raw_data, '-s', color="red")
ln4, = ax4.plot(time_data, temp_raw_data, '-P', color="brown")
ln5, = ax5.plot(time_data, humi_raw_data, '-*', color="slategrey")

# The following is to remove some navigation buttons 
# Full list of navigation buttons: forward, back, pan, zoom, home, help, subplots, save
buttons_names = ['forward', 'back', 'help', 'subplots']

for button in buttons_names:
    fig.canvas.manager.toolmanager.remove_tool(button)

print("Collecting data...")
start_time = time.time() # start the timer

count = 0

def update(i):

    global count

    count +=1

    while count <= (number_of_samples):
        # get the data from the arduino, decode it, and split it into a list
        get_data = serial_connection.readline()
        data_string = get_data.decode('utf-8')
        data_string_parsed = data_string[0:][:-2]
        readings = data_string_parsed.split(",")
        
        total_time = round((time.time() - start_time), 2)

        # add the raw data to their respective lists, converting to floats/ints
        co2_raw_data.append(float(readings[0]))
        voc_raw_data.append(int(readings[1]))
        nox_raw_data.append(int(readings[2]))
        temp_raw_data.append(float(readings[3]))
        humi_raw_data.append(float(readings[4]))
        time_data.append(total_time)

        print(f"Time: {total_time} (s), CO2: {float(readings[0])} (ppm), VOC: {float(readings[1])} (ppb), NOx: {float(readings[2])} (ppb), Temperature: {float(readings[3])} (\N{DEGREE SIGN}C), Humidity: {float(readings[4])} (%RH) \n")
    
        ln1.set_data(time_data, co2_raw_data)
        ln2.set_data(time_data, voc_raw_data)
        ln3.set_data(time_data, nox_raw_data)
        ln4.set_data(time_data, temp_raw_data)
        ln5.set_data(time_data, humi_raw_data)

        co2_raw_data_min = min(co2_raw_data)
        co2_raw_data_max = max(co2_raw_data)

        voc_raw_data_min = min(voc_raw_data)
        voc_raw_data_max = max(voc_raw_data)

        nox_raw_data_min = min(nox_raw_data)
        nox_raw_data_max = max(nox_raw_data)

        temp_raw_data_min = min(temp_raw_data)
        temp_raw_data_max = max(temp_raw_data)

        humi_raw_data_min = 0
        humi_raw_data_max = 100

        ax1.set_ylim(co2_raw_data_min - 100, co2_raw_data_max + 100)
        ax2.set_ylim(voc_raw_data_min - 100, voc_raw_data_max + 100)
        ax3.set_ylim(nox_raw_data_min - 100, nox_raw_data_max + 100)
        ax4.set_ylim(temp_raw_data_min - 100, temp_raw_data_max + 100)
        ax5.set_ylim(humi_raw_data_min, humi_raw_data_max)

        real_time_sample_counting = f"Samples left: {number_of_samples - count}"

        ax1.legend([float(readings[0])])
        ax2.legend([int(readings[1])])
        ax3.legend([int(readings[2])])
        ax4.legend([float(readings[3])])
        ax5.legend([float(readings[4])])

        fig.legends = []
        fig.legend([], title=real_time_sample_counting, frameon=False, loc="upper left")

        sns.despine()

        fig.tight_layout(pad=0.5)

        return ln1,

    if count == number_of_samples+1:
        # Combines the two lists as a tuple which can then be made into separate columns in a spreadsheet
        all_data = zip(time_data, co2_raw_data, voc_raw_data, nox_raw_data, temp_raw_data, humi_raw_data)

        # Adding the data to the CSV we created earlier
        with open(csv_file, 'w', encoding='UTF8', newline='') as f:
            data_headers = ["Time (s)", "CO2 (ppm)", "VOC (ppb)", "NOx (ppb)", "Temperature (oC)", "Humidity (%RH)"]

            writer = csv.writer(f)
            writer.writerow(data_headers)
            writer.writerows(all_data)

        file.close()

        print("Data collection is complete!")

animation = FuncAnimation(fig, update, interval=5500, blit=False, cache_frame_data=False)
plt.show()

# In case the user stops collecting samples early
if count < number_of_samples:
    all_data = zip(time_data, co2_raw_data, voc_raw_data, nox_raw_data, temp_raw_data, humi_raw_data) 

    # Adding the data to the CSV we created earlier
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        data_headers = ["Time (s)", "CO2 (ppm)", "VOC (ppb)", "NOx (ppb)", "Temperature (oC)", "Humidity (%RH)"]

        writer = csv.writer(f)
        writer.writerow(data_headers)
        writer.writerows(all_data)

    file.close()

    print("Data collection stopped early!")

