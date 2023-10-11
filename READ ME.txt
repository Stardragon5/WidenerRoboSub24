Hello Future Team!

We wanted to give you a few bits of information regarding the software since it is fairly complex, and will most likely only get more complex in the future. Please read below.

Arduino Code:
The current code from the Arduino has been uploaded. There are many different libraries that will have to be downloaded in order for the code to run (including the board too!). The only issues we could not solve was reading the depth sensor and efficiently sending data to the Rasp Pis. For the depth sensor, we believe it is an issue with the I2C communication since other onboard sensors use this as well. Here is the guide with information about the board: https://learn.adafruit.com/adafruit-feather-sense. The Serial comms to the Rasp Pi can probably be improved as well.

MATLAB:
The uploaded MATLAB folders are used for some testing with image processing. The Color_Samples folder holds the script that was used to identify the RGB ranges (by observation). More complex algorithms can be used to better identify colors or objects. For fun, we used some of the algorithms taught in our Vision course to see how things compare. These tests are in the ClusteringPCA Tests folder. Please talk with Prof. Song or another advisor to understand the applications of each algorithm and such.

WIDE1:
This folder holds the script files and some other modified files pulled from WIDE1. Not all the files were pulled, but this script is the one that is currently used for color recognition. This file and Rasp Pi will need significant overhaul to have better recognition ability. **Note: roscore needs to be run from WIDE2.

WIDE2:
This folder holds the script files and some other modified files pulled from WIDE2. In the Arduino Intake folder, pub2.py is the only fully functioning file. Other files were unsuccessful tests or outdated. This file reads the adafruit data and parses it. If more sensors are added or more data is sent, this file needs to be updated. In the Data Processing folder, sub.py is what reads the color values and moves the AUV based on time. This code will have to be updated to read other sensor data and determine position/heading. The motor test folder is where the eventual motor control will go. The initialize.py script must be run to setup the motors. There are more files on the physical Pi, but these are the main files that have been used. **Note: There are numerous commands to begin ros and start up packages and nodes. Visual studio is also installed on both Pis and is much better to run software. Some good resources for ros-based stuff are Prof. Shi and Prof. Hallahan.

Obviously, this is a lot to start with. If needed, please do not hesistate to reach out to the previous team for help. Prof. Song has all our information. Good luck, and please try to not sink the AUV...

~Team 22 from 2021-22
