#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

if __name__ == "__main__":
	arguments = get_arguments(('-m', "--mode", "mode", "Mode to Set"),
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	if not arguments.mode:
		display('-', "Please provide a mode!")
		exit(0)
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}")
	display('+', f"Mode               = {arguments.mode}", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	try:
		display('*', f"Setting mode to {arguments.mode}")
		mode_id = master.mode_mapping()[arguments.mode]
		master.set_mode(mode_id)
		print()
	except Exception as error:
		display('-', f"Failed to set mode to {arguments.mode} : ERROR => {error}")
		exit(0)

	while True:
		ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
		ack_msg = ack_msg.to_dict()
		if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
			continue
		display('+', mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
		break