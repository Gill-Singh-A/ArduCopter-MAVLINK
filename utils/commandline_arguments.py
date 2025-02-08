#! /usr/bin/env python3

from optparse import OptionParser

def get_arguments(*args):
	parser = OptionParser()
	for arg in args:
		parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
	return parser.parse_args()[0]

if __name__ == "__main__":
	pass
