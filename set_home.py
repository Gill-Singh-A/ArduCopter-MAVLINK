#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

def set_home(mavlink_connection, current_location=True, latitude=None, longitude=None, altitude=None, roll=0, pitch=0, yaw=0):
	data = [1, 0, 0, 0, 0, 0, 0] if current_location else [0, roll, pitch, yaw, latitude, longitude, altitude]
	mavlink_connection.mav.command_long_send(
		mavlink_connection.target_system,
		mavlink_connection.target_component,
		mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0,
		*data
	)

if __name__ == "__main__":
	arguments = get_arguments(('-l', "--latitude", "latitude", "Latitude"),
                              ('-L', "--longitude", "longitude", "Longitude"),
                              ('-a', "--altitude", "altitude", f"Altitude in meters (above home point)"),
                              ('-r', "--roll", "roll", "Roll (Default=0)"),
                              ('-p', "--pitch", "pitch", "Pitch (Default=0)"),
                              ('-y', "--yaw", "yaw", "Yaw (Default=0)"),
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]
	if not arguments.latitude or not arguments.longitude or not arguments.altitude:
		current_position = True
	else:
		home_latitude, home_longitude, home_altitude = float(arguments.latitude), float(arguments.longitude), float(arguments.altitude)
	home_roll = float(arguments.roll) if arguments.roll else 0
	home_pitch = float(arguments.pitch) if arguments.pitch else 0
	home_yaw = float(arguments.yaw) if arguments.yaw else 0

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display('*', f"Setting Home...")
	set_home(master, current_position, home_latitude, home_longitude, home_altitude, home_roll, home_pitch, home_yaw)
	display("+", f"Done!")
