#! /usr/bin/env python3

from datetime import date
from colorama import Fore, Back, Style
from time import strftime, localtime, sleep

status_color = {
	'+': Fore.GREEN,
	'-': Fore.RED,
	'*': Fore.YELLOW,
	':': Fore.CYAN,
	' ': Fore.WHITE
}

def display(status, data, start='', end='\n'):
	print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

if __name__ == "__main__":
	pass
