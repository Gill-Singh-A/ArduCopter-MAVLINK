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
	"acceleration": 3128,
	"position+velocity": 3520,
	"position+velocity+acceleration": 3072,
	"yaw": 2559,
	"yaw_rate": 1535
}

def goto_global_position(mavlink_connection, global_latitude, global_longitude, altitude, yaw=0, tolerance=0.1, global_tolerance=0.00005, type_mask="position"):
	mavlink_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(
		10, mavlink_connection.target_system, mavlink_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, type_masks[type_mask],
		int(global_latitude * 10 ** 7), int(global_longitude * 10 ** 7), altitude, 0, 0, 0, 0, 0, 0, yaw, 0
	))
	while True:
		message = mavlink_connection.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
		current_lat, current_lon, current_alt, current_rel_alt, current_vx, current_vy, current_vz, current_hdg = message.lat, message.lon, message.alt, message.relative_alt, message.vx, message.vy, message.vz, message.hdg
		display(':', f"Latitude = {current_lat/(10**7)}, Longitude = {current_lon/(10**7)}, Altitude = {current_alt}, Relative Altitude = {current_rel_alt}\t Vx = {current_vx:.2f}, Vy = {current_vy:.2f}, Vz = {current_vz:.2f}\tYaw = {current_hdg}")
		if distance([global_latitude, global_longitude], [current_lat, current_lon]) < global_tolerance and distance([altitude], [current_rel_alt]) < tolerance:
			break

if __name__ == "__main__":
	arguments = get_arguments(('-l', "--latitude", "latitude", "Latitude"),
                              ('-L', "--longitude", "longitude", "Longitude"),
                              ('-a', "--altitude", "altitude", f"Altitude in meters (above home point)"),
                              ('-y', "--yaw", "yaw", f"Yaw (Default={configuration['yaw']})"),
                              ('-t', "--position-tolerance", "position_tolerance", f"Position Tolerance (in meters, Default={configuration['position_tolerance']})"),
							  ('-g', "--global-position-tolerance", "global_position_tolerance", f"Global Position Tolerance (Default={configuration['global_position_tolerance']})")
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]
	if not arguments.latitude or not arguments.longitude or not arguments.altitude:
		display('-', "Please Enter a Valid Position")
		exit(0)
	latitude, longitude, altitude = float(arguments.latitude), float(arguments.longitude), float(arguments.altitude)
	yaw = float(arguments.yaw) if arguments.yaw else configuration["yaw"]
	position_tolerance = float(arguments.position_tolerance) if arguments.position_tolerance else configuration["position_tolerance"]
	global_position_tolerance = float(arguments.global_position_tolerance) if arguments.global_position_tolerance else configuration["global_position_tolerance"]

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}")
	display('+', f"GLOBAL POSITION    = ({latitude}, {longitude})", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display('*', f"Going to Position => ({latitude}, {longitude}) with Yaw : {yaw}")
	goto_global_position(master, latitude, longitude, altitude, yaw=yaw, tolerance=position_tolerance, global_tolerance=global_position_tolerance)
	display("+", f"Done!")
