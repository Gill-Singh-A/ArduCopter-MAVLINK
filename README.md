# ArduCopter MAVLINK
This repository contains simple python scripts that controls ArduPilot via MAVLINK by doing some simple operations using an onboard computer through Serial Communication
## Setup
To setup a [Raspberry-Pi](https://www.raspberrypi.org) follow the setups present in [MAVLINK Rasberry Pi Setup](setup.md)
## Install Python Dependencies
```
sudo pip3 install -r requirements.txt
```
Dependencies:
* pyserial
* MAVProxy
* colorama
* pymavlink
## Configuration
Default Configurations are present in file **[config.json](config.json)** which contains:
* Connection
* Baudrate
* Takeoff Altitude
* Yaw
* Position Tolerance
<!-- -->
You can change these values according to your system and usage.<br />
The command line arguments to change these values are present in every python program in this repository
## Command Line Arguments
Every Script have 2 command line arguments in common:
* Connection: Serial Device for MAVLINK
* Baudrate: Baudrate for MAVLINK Connection
<!-- -->
Some programs have extra command line arguments
### takeoff.py
* altitude: Takeoff Altitude
### set_mode.py
* mode: Mode to Set
### set_home.py
* latitude: Latitude
* longitude: Longitude
* altitude: Altitude in meters (above home point)
* roll: Roll
* pitch: Pitch
* yaw: Yaw
### set_speed.py
* set-speed: Speed to Set (in meters/second)
* speed-type: Speed Types
### local_position.py
* x: Distance to Move in North (in meters)
* y: Distance to Move in East (in meters)
* z: Distance to Move Down (in meters)
* yaw: Yaw
* position-tolerance: Position Tolerance (in meters)
### global_position.py
* latitude: Latitude
* longitude: Longitude
* altitude: Altitude in meters (above home point)
* yaw: Yaw
* position-tolerance: Position Tolerance (in meters)
# References
* [Mission Commands](https://ardupilot.org/dev/docs/common-mavlink-mission-command-messages-mav_cmd.html)
* [MAVLink Developer Guide](https://mavlink.io/en/)
* [ArduPilot Docs](https://ardupilot.org/dev/docs/)