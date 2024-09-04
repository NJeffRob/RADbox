# RADbox
Github repository to host the Arduino, python and executables for the Real-time Air Data box (RADbox) project. **This project is not being actively maintained so users who are modifying the source code are on their own.**

## Table of Contents
- [Source Code Installation](#source-code-installation)
- [Executable Installation](#executable-installation)
- [Use](#use)

### Source Code Installation
The source code (arduino and python) can be found in the "source_code" directory. To modify/run this code manually, the following dependencies are required:
- **Python**:
  - pyserial v3.5 [pyserial](https://pyserial.readthedocs.io/en/latest/)
  - matplotlib v3.6.3 [matplotlib](https://matplotlib.org/stable/index.html)
  - seaborn v0.12.1 [seaborn](https://seaborn.pydata.org/)

- **Arduino**:
  - Sparkfun SCD4x Arduino Library v1.1.2 [Sparkfun SCD4x Arduino Library](https://github.com/sparkfun/SparkFun_SCD4x_Arduino_Library)
  - Sensirion I2C SGP41 library v1.0.0 [Sensirion I2C SGP41 library](https://github.com/Sensirion/arduino-i2c-sgp41)
  - DFRobot_DHT20 library v1.0.0 [DFRobot_DHT20 library](https://github.com/DFRobot/DFRobot_DHT20)
  - (for RADbox) U8glib library v1.19.1 [U8glib library](https://github.com/olikraus/u8glib)

Note that code was written in Python 3.11.9 and Arduino version 2.2.1.

Using the source code directly is possible so long as the user has a version of Python (at least 3.11) and Arduino is installed. Prepare the relevant Arduino by uploading the relevant .ino file to the board. For Python, simply run the following command in a terminal, or run it through a chosen IDE, to have it run:

```python
python Radbox.py
```
or
```python
python Radbox_lite.py
```

Note that it's convenient to make a separate folder to both keep and run this code, as a .csv file will be created after every run.

### Executable Installation
You can find the Executables for both Windows and Linux under the *Releases* tab of this repository. To use these, first download and unzip them for your relevant operating system. Next, upload the relevant .ino file to the board. After this, the executable files can simply be run and the program will start. Note that it's convenient to make a separate folder to both keep and run the executable, as a .csv file will be created after every run.

### Use
The RADbox was designed to teach students in the K-12 system about air-quality. It is capable of monitoring changes in CO<sub>2</sub>, VOCs, NO<sub>x</sub>, temperature and %humidity. To use the device, simply plug it in, run the software, and collect the relevant data (after appropridate setup - see [Source Code Installation](#source-code-installation) and [Executable Installation](#executable-installation)). For a thorough guide, please see the published paper.





