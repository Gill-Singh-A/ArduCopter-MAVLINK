#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

if __name__ == "__main__":
	arguments = get_arguments(('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display(':', "DISARMING DRONE...")
	master.arducopter_disarm()
	master.motors_disarmed_wait()
	display('+', "DISARMED!")