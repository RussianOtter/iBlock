"""
 _ _____ _         _   
|_| __  | |___ ___| |_ 
| | __ -| | . |  _| '_|
|_|_____|_|___|___|_,_|

iBlock is a machine learning video game!
This game is played on a 8x6 board (48 spaces) and the goal is to fill up the enemy's column with your pieces! Once that happens the game will reset and log all the data for the AI's to observe! In the first few games the AI will take random moves and attempt winning. Once one of the AI's win, the information on how they one gets processed and they try to attempt it again using that information!

Rather then focusing on attacking, these AI naturally plays offensively! You will see them defend their base while at the same time try to attack the enemy!
The AI also doesn't know which spaces it must fill to win so as it plays it must learn on it's own (this also allows for the creation of custom maps).

iBlock has multiple different game options for how to set up the way the AI will play! New gamemodes coming soon!

Copyright (c) SavSec 2017
Copyright (c) SavSec iBlock 2017

Format:
	Encoding: UTF-8
	Tab: 2
System:
	Python 2.7
	Modules: sys, time, random
License:
	MIT License
Developer:
	@Russian_Otter - Instagram

"""

import sys, random, time, argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--intelligence",help="Activates dynamic machine learning mode for both players",action="store_true")
parser.add_argument("-r", "--random",help="Activates random machine learning mode for both players",action="store_true")
parser.add_argument("-p", "--pvai",help="Activates Player vs AI mode",action="store_true")
parser.add_argument("-R", "--Reset",help="Activates reset mode for both players",action="store_true")
parser.add_argument("-sm", "--show-moves",help="Shows the last move for each turn",action="store_true")
parser.add_argument("-d", "--display",help="Set to False to disable table display",default=True)
parser.add_argument("-pg", "--progress",help="Displays progress graphs", action="store_true")
parser.add_argument("-t", "--time",help="Turn rate for each player",default=0.05)
parser.add_argument("-q", "--quick",help="Plays a 1 match game", action="store_true")
parser.add_argument("-H", "--Hide",help="Hides help",action="store_true")
args = parser.parse_args()

if args.pvai:
	human_mode = True
else:
	human_mode = False
if args.Reset:
	fresh_start1,fresh_start0 = True,True
else:
	fresh_start0,fresh_start1 = False,False
if args.show_moves:
	show_move = True
else:
	show_move = False
if args.progress:
	progress_graphing = True
else:
	progress_graphing = False
display = args.display
mtime = float(args.time)

if show_move:
	from time import gmtime, strftime
if progress_graphing:
	"""
	import matplotlib.pyplot as plt
	import numpy as np
	Still in progress
	"""
	pass

global last_move
last_move = ["41"]

def pull_dynamics(player):
	p0_info = open("player_0.ib").read().split()
	p1_info = open("player_1.ib").read().split()
	if player == "1":
		return p1_info
	if player == "0":
		return p0_info

def table_ref():
	print """
       Table Reference
==============================
1  |2 | 3   4   5   6  |7 | 8
9  |10| 11  12  13  14 |15| 16
17 |18| 19  20  21  22 |23| 24
25 |26| 27  28  29  30 |31| 32
33 |34| 35  36  37  38 |39| 40
41 |42| 43  44  45  46 |47| 48
==============================
"""
	pass
		

table = {
	"1":".",  "2":".",  "3":".",  "4":".",  "5":".",  "6":".",  "7":".",  "8":"0",
	"9":".", "10":".", "11":".", "12":".", "13":".", "14":".", "15":".", "16":".",
	
	"17":".", "18":".", "19":".", "20":".", "21":".", "22":".", "23":".", "24":".",
	"25":".", "26":".", "27":".", "28":".", "29":".", "30":".", "31":".", "32":".",
	
	"33":".", "34":".", "35":".", "36":".", "37":".", "38":".", "39":".", "40":".",
	"41":"1", "42":".", "43":".", "44":".", "45":".", "46":".", "47":".", "48":"."
}

# up left    = -9
# up down    = +-8
# right left = +-1
# down right = +9
# up right   = -7
# down left  = +7


def table_reset():
	reset = {
	"1":".",  "2":".",  "3":".",  "4":".",  "5":".",  "6":".",  "7":".",  "8":"0",
	"9":".", "10":".", "11":".", "12":".", "13":".", "14":".", "15":".", "16":".",
	
	"17":".", "18":".", "19":".", "20":".", "21":".", "22":".", "23":".", "24":".",
	"25":".", "26":".", "27":".", "28":".", "29":".", "30":".", "31":".", "32":".",
	
	"33":".", "34":".", "35":".", "36":".", "37":".", "38":".", "39":".", "40":".",
	"41":"1", "42":".", "43":".", "44":".", "45":".", "46":".", "47":".", "48":"."
}
	table.update(reset)

def table_print(table):
	if display:
		print "\n"+"=" * 26
		print """%s  .%s.  %s  %s  %s  %s  .%s.  %s  
%s  .%s.  %s  %s  %s  %s  .%s.  %s  
%s  .%s.  %s  %s  %s  %s  .%s.  %s  
%s  .%s.  %s  %s  %s  %s  .%s.  %s  
%s  .%s.  %s  %s  %s  %s  .%s.  %s  
%s  .%s.  %s  %s  %s  %s  .%s.  %s""".replace(".","|") %(
	table["1"],table["2"],table["3"],table["4"],table["5"],table["6"],table["7"],table["8"],
	table["9"],table["10"],table["11"],table["12"],table["13"],table["14"],table["15"],table["16"],
	table["17"],table["18"],table["19"],table["20"],table["21"],table["22"],table["23"],table["24"],
	table["25"],table["26"],table["27"],table["28"],table["29"],table["30"],table["31"],table["32"],
	table["33"],table["34"],table["35"],table["36"],table["37"],table["38"],table["39"],table["40"],
	table["41"],table["42"],table["43"],table["44"],table["45"],table["46"],table["47"],table["48"]
	)
		print "=" * 26

def my_blocks(id):
	block = []
	id = str(id)
	for _ in table:
		if table[_] == id:
			block.append(_)
	return block

def grab_dynamics(player):
	if player == "0":
		dyn = open("player_0.ib").read().split(" ")
	if player == "1":
		dyn = open("player_1.ib").read().split(" ")
	return dyn

def sort_dynamics(latest,player):
	info = latest+grab_dynamics(player)
	return list(set([x for x in info if info.count(x) > 1]))
 
def write_dynamics(dynamics,player):
	if player == "0":
		dyn = open("player_0.ib","w")
		dyn.write(" ".join(dynamics))
		dyn.close()
	if player == "1":
		dyn = open("player_1.ib","w")
		dyn.write(" ".join(dynamics))
		dyn.close()

def move(id,space,table=table):
	table.update({space:id})
	last_move = space
	table_print(table)
	if show_move:
		tplay = strftime("%H:%M:%S", gmtime())
		print "[%s] Player %s moved to %s" %(tplay,id,space)
	time.sleep(mtime)
	return last_move

def validate_move(space,id,attempt=0):
	if attempt == 5:
		return True
	if table[space] != id:
		if space in globals()["last_move"]:
			return False
		return True
	else:
		return False

def move_options(space,player="3"):
	space = str(space)
	tspace = int(space)
	if space in [
		"10","11","12","13","14","15",
		"18","19","20","21","22","23",
		"26","27","28","29","30","31",
		"34","35","36","37","38","39",
		]:
		moves = tspace-9,tspace+9,tspace-7,tspace+7,tspace-8,tspace+8,tspace+1,tspace-1
	if space == "1":
		moves = tspace+1,tspace+8,tspace+9
	if space == "8":
		moves = tspace-1,tspace+8,tspace+7
	if space == "41":
		moves = tspace+1,tspace-8,tspace-7
	if space == "48":
		moves = tspace-1,tspace-8,tspace-9
	if space in ["2","3","4","5","6","7"]:
		moves = tspace+8,tspace-1,tspace+1,tspace+7,tspace+9
	if space in ["16","24","32","40"]:
		moves = tspace-1,tspace-8,tspace+8,tspace-9,tspace+7
	if space in ["9","17","25","33"]:
		moves = tspace+1,tspace+8,tspace-8,tspace+9,tspace-7
	if space in ["42","43","44","45","46","47"]:
		moves = tspace-1,tspace+1,tspace-8,tspace-9,tspace-7
	
	area = []
	for _ in moves:
		if table[str(_)] != player:
			area.append(str(_))
	return area

def available_moves(player):
	moves = []
	m = 0
	for _ in my_blocks(player):
		for v in move_options(_):
			if table[v] != player:
				moves.insert(m,v)
				m += 1
	return moves

def dynamic_update(new,old,player):
	info = new + old
	for _ in new:
		info.append(_)
	return list(set([x for x in info if info.count(x) > 1]))

def push_dynamics(dyn,player):
	if player == "1":
		cv = open("player_1.ib").read().split(" ")
		dyn = dynamic_update(cv,dyn,"1")
		print dyn
		f = open("player_1.ib","w")
		f.write("")
		f.write(" ".join(dyn))
		f.close()
		print "\nUpdated Values:\n"+open("player_1.ib").read()
		time.sleep(2)
	
	if player == "0":
		cv = open("player_0.ib").read().split(" ")
		dyn = dynamic_update(cv,dyn,"0")
		f = open("player_0.ib","w")
		f.write("")
		f.write(" ".join(dyn))
		f.close()
		print "\nUpdated Values:\n"+open("player_0.ib").read()
		time.sleep(2)

def check_for_win(dinfo0,dinfo1,real=True,table=table,push=False,fresh_start0=fresh_start0,fresh_start1=fresh_start1):
	if table["2"] + table["10"] + table["18"] + table["26"] + table["34"] + table["42"] == "000000":
		if fresh_start0:
			f = open("player_0.ib","w")
			f.write(" ".join(my_blocks("0")))
			f.close()
			fresh_start0 = False
		else:
			if push:
				write_dynamics(sort_dynamics(my_blocks("0"),"0"),"0")
		
		print "Player 0 Wins!"
		p0_info = open("player_0.ib").read().split()
		p1_info = open("player_1.ib").read().split()
		pf0 = 48-len(p0_info)
		pf1 = 48-len(p1_info)
		if pf0 == 48:
			pf0 = 0
		if pf1 == 48:
			pf1 = 0
		print "Player 0 Fitness:",pf0
		print "Player 1 Fitness:",pf1
		time.sleep(2)
		if real:
			sys.exit()
		else:
			table_reset()
			return True,"0"
	
	if table["7"] + table["15"] + table["23"] + table["31"] + table["39"] + table["47"] == "111111":
		if fresh_start1:
			f = open("player_1.ib","w")
			f.write(" ".join(my_blocks("1")))
			f.close()
			fresh_start1 = False
		else:
			if push:
				write_dynamics(sort_dynamics(my_blocks("1"),"1"),"1")
		
		print "Player 1 Wins!"
		p0_info = open("player_0.ib").read().split()
		p1_info = open("player_1.ib").read().split()
		pf0 = 48-len(p0_info)
		pf1 = 48-len(p1_info)
		if pf0 == 48:
			pf0 = 0
		if pf1 == 48:
			pf1 = 0
		print "Player 0 Fitness:",pf0
		print "Player 1 Fitness:",pf1
		time.sleep(2)
		if real:
			sys.exit()
		else:
			table_reset()
			return True,"1"

def last_go(last):
	globals()["last_move"].append(last)
	if len(last_move) > 2:
		globals()["last_move"].reverse()
		globals()["last_move"].pop(1)
		globals()["last_move"].reverse()

def iblock(real=False,dynamic=False):
	push = True
	dyn0,dyn1 = [],[]
	p0w,p1w = 0,0
	while 1:
		for _ in "1","0":
			dyn0 = my_blocks("0")
			dyn1 = my_blocks("1")
			
			if p0w == 5:
				check = check_for_win(dyn0,dyn1, real=real,push=True)
				p0w = 0
			if p1w == 5:
				check = check_for_win(dyn0,dyn1, real=real,push=True)
				p1w = 0
			if p0w < 5 and p1w < 5:
				check = check_for_win(dyn0,dyn1, real=real,push=push)
			
			if "None" in str(type(check)):
				check = [dynamic,_]
			
			if check[0]:
				if check[1] == "1":
					p1w += 1
				if check[1] == "0":
					p0w += 1
				dyn = pull_dynamics(check[1])
				if check[1] == "0":
					dyn0 = dynamic_update(dyn,dyn0,"0")
				if check[1] == "1":
					dyn1 = dynamic_update(dyn,dyn1,"1")
				
			go_move,block = None,None
			if _ == "0":
				av = available_moves(_)
				try:
					if type(av) == tuple:
						av = list(av)
					for lm in last_move:
						av.pop(av.index(lm))
				except:
					pass
				for md in dyn0:
					if md in av:
						go_move = md
			if _ == "1":
				av = available_moves(_)
				try:
					if type(av) == tuple:
						av = list(av)
					for lm in last_move:
						av.pop(av.index(lm))
				except:
					pass
				for md in dyn1:
					if md in av:
						go_move = md
			
			if go_move == None:
				block = True
			
			attempt = -1
			while 1:
				attempt += 1
				try:
					if block == None:
						c = go_move
					else:
						c = random.choice(available_moves(_))
					if attempt > 2:
						c = random.choice(available_moves(_))
					if validate_move(c,_,attempt) == True:
						break
				except Exception as e:
					print e
					c = random.choice(available_moves(_))
			last_go(move(_,c))

def iblockgo(real=False,dynamic=False):
	push = True
	dyn0,dyn1 = [],[]
	p0w,p1w = 0,0
	while 1:
		for _ in "1","0":
			dyn0 = my_blocks("0")
			dyn1 = my_blocks("1")
			
			if p0w == 5:
				check = check_for_win(dyn0,dyn1, real=real,push=True)
				p0w = 0
			if p1w == 5:
				check = check_for_win(dyn0,dyn1, real=real,push=True)
				p1w = 0
			if p0w < 5 and p1w < 5:
				check = check_for_win(dyn0,dyn1, real=real,push=push)
			
			if "None" in str(type(check)):
				check = [dynamic,_]
			
			if check[0]:
				if check[1] == "1":
					p1w += 1
				if check[1] == "0":
					p0w += 1
				dyn = pull_dynamics(check[1])
				if check[1] == "0":
					dyn0 = dynamic_update(dyn,dyn0,"0")
				if check[1] == "1":
					dyn1 = dynamic_update(dyn,dyn1,"1")
				
			go_move,block = None,None
			if _ == "0":
				av = available_moves(_)
				try:
					if type(av) == tuple:
						av = list(av)
					for lm in last_move:
						av.pop(av.index(lm))
				except:
					pass
				for md in dyn0:
					if md in av:
						go_move = md
			if _ == "1":
				av = available_moves(_)
				try:
					if type(av) == tuple:
						av = list(av)
					for lm in last_move:
						av.pop(av.index(lm))
				except:
					pass
				for md in dyn1:
					if md in av:
						go_move = md
			
			if go_move == None:
				block = True
			
			if _ == "1":
				table_ref()
				print "Available Moves:"
				for av in available_moves(_):
					print av,
				print
				while 1:
					go_move = raw_input("iBlock ~ ")
					if go_move in available_moves(_) and validate_move(go_move,_):
						last_go(move(_,go_move))
						break
			else:
				attempt = -1
				while 1:
					attempt += 1
					try:
						if block == None:
							c = go_move
						else:
							c = random.choice(available_moves(_))
						if attempt > 2:
							c = random.choice(available_moves(_))
						if validate_move(c,_,attempt) == True:
							break
					except Exception as e:
						print e
						c = random.choice(available_moves(_))
				last_go(move(_,c))

def reset_knowldge():
	"""
	Reseting knowldge wipes all past game history and updates it with random winning moves.
	"""
	print "Reseting Knowldge..."
	time.sleep(1)
	
	if not fresh_start0 or not fresh_start1:
		print "You must change values: \"fresh_start0\" and \"fresh_start1\" to True before reseting."
		print "Be sure to change those values back to False while not in reset mode."
		time.sleep(3)
		
	if mtime > 0.0009 or display == True:
		print "Consider Temporarily Changing You Game Settings For Reset:"
		print "-Speed should be less than 0.0009"
		print "-Display should be turned off"
		time.sleep(3)
	try:
		iblock(False,False)
	except:
		pass
	print "Reset Complete!"
	time.sleep(1)

def random_ai_mode():
	"""
	Random AI mode disables the learning ability of the program which causes it to make random moves.
	(Personally this is more entiretaining than Intelligence Mode)
	"""
	print "Starting Random AI Mode..."
	if mtime < 0.05:
		print "Consider changing the frame rate to more than 0.05 while in random mode"
		time.sleep(3)
	if display == False:
		print "Consider changing display to True inorder to view the game in random mode"
		time.sleep(3)
	time.sleep(1)
	try:
		iblock(False,False)
	except:
		print "Game Paused"

def intelligence_mode():
	if mtime < 0.005:
		print "Consider changing the frame rate to more than 0.005 while in intelligence mode"
		time.sleep(3)
	if display == False:
		print "Consider changing display to True inorder to view the game in intelligence mode"
		time.sleep(3)
	"""
	This mode activates the intelligence factor of the machine learning program and tells it to improve based on it's last victories!
	"""
	print "Starting Intelligence Mode..."
	time.sleep(1)
	try:
		iblock(False,True)
	except:
		print "Game Paused"

def intelligent_1v1():
	"""
	This is a 1 match mode to quickly see who wins a fast fight
	"""
	print "Starting Intelligent 1v1..."
	if mtime < 0.005:
		print "Consider changing the frame rate to more than 0.005 while in intelligence mode"
		time.sleep(3)
	if display == False:
		print "Consider changing display to True inorder to view the game in intelligence mode"
		time.sleep(3)
	time.sleep(1)
	try:
		iblock(True,True)
	except:
		print "Game Paused"

def human_vs_iblock():
	"""
	You'll probably loose...
	"""
	# Coming Soon #

if not args.Hide:
	print """
 _ _____ _         _   
|_| __  | |___ ___| |_ 
| | __ -| | . |  _| '_|
|_|_____|_|___|___|_,_|
"""
	parser.print_help()
	print
	print "Available Game Modes/Options:"
	print "-Random Mode"
	print "-Intelligence Mode"
	print "-1 Match Intelligence Mode"
	print "-Reset Mode"
	print "-Human vs Player Mode"
	print "\n(Enter the function name for the gamemode you want in the python terminal or set your arguments to choose your gamemode)\n"
	print "Set arguments to \"-H\" to disable this message."
	time.sleep(0.5)

if len(sys.argv) > 1:
	if args.intelligence:
		intelligence_mode()
		sys.exit()
	if args.random:
		random_ai_mode()
		sys.exit()
	if args.Reset:
		print "Stop the program once both player's fitness is at your desired stat"
		reset_knowldge()
		sys.exit()
	if args.quick:
		intelligent_1v1()
		sys.exit()
	if human_mode:
		try:
			iblockgo()
		except:
			print "Game Paused/Stopped"
