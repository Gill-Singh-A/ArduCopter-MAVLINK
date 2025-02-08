#! /usr/bin/env python3

def distance(position_1, position_2):
	position_distance = 0
	for component_1, component_2 in zip(position_1, position_2):
		position_distance += component_1 ** 2 + component_2 ** 2
	return position_distance ** 0.5

if __name__ == "__main__":
	pass