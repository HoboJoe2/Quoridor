"""Includes strings used in other files"""

from colorama import Fore, Back, Style

welcome = """
Welcome to Quoridor, type help to see a list of commands.

Note that this program isn't finished, if one player lands on another player's
piece everyone should type "pass" until it's the players turn again. Also,
once someone wins type "exit" to exit the program.
"""

help = """
Commands:

help > Shows this wall of text.
start > Starts a new game.
rules > Prints the rules.
"""

rules = """
Go to https://www.ultraboardgames.com/quoridor/game-rules.php to see the rules.
"""

move_help = f"""
Input moving your peice like this:

m_n -> move north
m_e -> move east

Input placing a wall like this:

w_h_2_3 -> Horizontal wall at row 2, column 3
w_v_8_5 -> Vertical wall at row 8, column 5

Walls will be placed from the top left point of the coordinate you
specify, going south or east.
For example, if blue played w_h_1_1 and red played w_v_1_1 the result would be:

      {Fore.LIGHTBLACK_EX}1 2{Fore.RESET}
     +{Fore.BLUE}-+-{Fore.RESET}+
   {Fore.LIGHTBLACK_EX}1{Fore.RESET} {Fore.RED}|{Fore.BLACK}O{Fore.RESET}|{Fore.BLACK}O{Fore.RESET}|
     {Fore.RED}+{Fore.RESET}-+-+
   {Fore.LIGHTBLACK_EX}2{Fore.RESET} {Fore.RED}|{Fore.BLACK}O{Fore.RESET}|{Fore.BLACK}O{Fore.RESET}|
     +-+-+
"""
