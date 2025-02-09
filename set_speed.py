#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

speed_types = {
	None: 0,
	"horizontal": 1,
	"climb": 2,
	"descent": 3
}

def set_drone_speed(mavlink_connection, speed, speed_type="horizontal"):
	mavlink_connection.mav.command_long_send(
		mavlink_connection.target_system,
		mavlink_connection.target_component,
		mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0,
		speed_types[speed_type], speed, 0, 0, 0, 0, 0
	)

if __name__ == "__main__":
	arguments = get_arguments(('-s', "--set-speed", "set_speed", "Speed to Set (in meters/second)"),
                              ('-t', "--speed-type", "speed_type", f"Speed Types (Default=horizontal, Available Options = {list(speed_types.keys())})"),
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]
	if not arguments.set_speed:
		display('-', "Please Enter a Valid Speed")
		exit(0)
	else:
		set_speed = float(arguments.set_speed)

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display('*', f"Setting Speed => {set_speed} meters/second")
	set_drone_speed(master, set_speed, arguments.speed_type)
	display("+", f"Done!")