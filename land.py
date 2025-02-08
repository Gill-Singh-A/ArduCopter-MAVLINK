#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.distance import distance
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

def land(mavlink_connection):
	mavlink_connection.mav.command_long_send(
		mavlink_connection.target_system,
		mavlink_connection.target_component,
		mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
		0, 0, 0, 0, 0, 0, 0
	)
	while True:
		message = mavlink_connection.recv_match(type="LOCAL_POSITION_NED", blocking=True)
		current_x, current_y, current_z, current_vx, current_vy, current_vz = message.x, message.y, message.z, message.vx, message.vy, message.vz
		display(':', f"X = {current_x:.2f}, Y = {current_y:.2f}, Z = {current_z:.2f}\t Vx = {current_vx:.2f}, Vy = {current_vy:.2f}, Vz = {current_vz:.2f}")
		if distance([0.0, 0.0, 0.0], [current_x, current_y, current_z]) < configuration["position_tolerance"]:
			break

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

	display('*', f"LANDING...")
	land(master)
	display('+', f"LANDED!")