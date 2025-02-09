#! /usr/bin/env python3

import json
from pymavlink import mavutil

from utils.display import display
from utils.distance import distance
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

type_masks = {
	"position": 3576,
	"velocity": 3527,
	"acceleration": 3135,
	"position+velocity": 3520,
	"position+velocity+acceleration": 3072,
	"yaw": 2559,
	"yaw_rate": 1535
}

def goto_local_position(mavlink_connection, local_x, local_y, local_z, yaw=0, tolerance=0.1, type_mask="position"):
	mavlink_connection.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
		10, mavlink_connection.target_system, mavlink_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, type_masks[type_mask],
		local_x, local_y, local_z, 0, 0, 0, 0, 0, 0, yaw, 0
	))
	while True:
		message = mavlink_connection.recv_match(type="LOCAL_POSITION_NED", blocking=True)
		current_x, current_y, current_z, current_vx, current_vy, current_vz = message.x, message.y, message.z, message.vx, message.vy, message.vz
		display(':', f"X = {current_x:.2f}, Y = {current_y:.2f}, Z = {current_z:.2f}\t Vx = {current_vx:.2f}, Vy = {current_vy:.2f}, Vz = {current_vz:.2f}")
		if distance([local_x, local_y, local_z], [current_x, current_y, current_z]) < tolerance:
			break

if __name__ == "__main__":
	arguments = get_arguments(('-x', "--north", "x", "Distance to Move in North (in meters)"),
                              ('-y', "--east", "y", "Distance to Move in East (in meters)"),
                              ('-z', "--down", "z", "Distance to Move Down (in meters)"),
                              ('-y', "--yaw", "yaw", f"Yaw (Default={configuration['yaw']})"),
                              ('-t', "--position-tolerance", "position_tolerance", f"Position Tolerance (in meters, Default={configuration['position_tolerance']})"),
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]
	if not arguments.x or not arguments.y or not arguments.z:
		display('-', "Please Enter a Valid Position")
		exit(0)
	x, y, z = float(arguments.x), float(arguments.y), float(arguments.z)
	yaw = float(arguments.yaw) if arguments.yaw else configuration["yaw"]
	position_tolerance = float(arguments.position_tolerance) if arguments.position_tolerance else configuration["position_tolerance"]

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}")
	display('+', f"LOCAL POSITION     = ({x}, {y}, {z}) meters", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display('*', f"Going to Position => ({x}, {y}, {z}) [North, East, Down] with Yaw : {yaw}")
	goto_local_position(master, x, y, z, yaw=yaw, tolerance=position_tolerance)
	display("+", f"Done!")