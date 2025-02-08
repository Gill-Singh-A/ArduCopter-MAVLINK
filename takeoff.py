#! /usr/bin/env python3

import json
from time import sleep
from pymavlink import mavutil

from utils.display import display
from utils.distance import distance
from utils.commandline_arguments import get_arguments

with open("config.json", 'r') as file:
	configuration = json.load(file)

def takeoff(mavlink_connection, altitude, wait=10):
	mavlink_connection.mav.command_long_send(
		mavlink_connection.target_system,
		mavlink_connection.target_component,
		mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
		0, 0, 0, 0, 0, 0, 0, altitude
	)
	while True:
		message = mavlink_connection.recv_match(type="LOCAL_POSITION_NED", blocking=True)
		current_x, current_y, current_z, current_vx, current_vy, current_vz = message.x, message.y, message.z, message.vx, message.vy, message.vz
		display(':', f"X = {current_x:.2f}, Y = {current_y:.2f}, Z = {current_z:.2f}\t Vx = {current_vx:.2f}, Vy = {current_vy:.2f}, Vz = {current_vz:.2f}")
		if distance([0.0, 0.0, 0.0], [current_x, current_y, current_z]) < configuration["position_tolerance"]:
			break

if __name__ == "__main__":
	arguments = get_arguments(('-a', "--altitude", "altitude", "Takeoff Altitude (in meters, Default=configuration['takeoff_altitude'])"),
                              ('-c', "--connection", "connection", f"Serial Device for MAVLINK (Default={configuration['connection']})"),
                              ('-b', "--baudrate", "baudrate", f"Baudrate for MAVLINK Connection (Default={configuration['baudrate']})"))
	arguments.connection = arguments.connection if arguments.connection else configuration["connection"]
	arguments.baudrate = int(arguments.baudrate) if arguments.baudrate else configuration["baudrate"]
	arguments.altitude = float(arguments.altitude) if arguments.altitude else configuration["takeoff_altitude"]

	display(':', f"MAVLINK Connection = {arguments.connection}")
	display(':', f"MAVLINK Baudrate   = {arguments.baudrate}")
	display('+', f"TAKEOFF ALTITUDE   = {arguments.altitude} meters", end='\n\n')

	display('*', "Connecting to MAVLINK...")
	master = mavutil.mavlink_connection(arguments.connection, arguments.baudrate)
	display('*', "Waiting for Heartbeat...")
	master.wait_heartbeat()
	display('+', "Heartbeat Received")
	display(':', f"\tSYSTEM    => {master.target_system}")
	display(':', f"\tCOMPONENT => {master.target_component}", end='\n\n')

	display('*', "ARMING DRONE...")
	master.arducopter_arm()
	master.motors_armed_wait()
	display('+', "ARMED!", end='\n\n')

	sleep(2)
	display('*', f"TAKING OFF TO {arguments.altitude} meters ...")
	takeoff(master, arguments.altitude)
	display('+', f"Done TAKE OFF!")