iBlock
======

iBlock is a machine learning video game!

This game is played on a 8x6 board (48 spaces) and the goal is to fill up the enemy's column with your pieces! Once that happens the game will reset and log all the data for the AI's to observe! In the first few games the AI will take random moves and attempt winning. Once one of the AI's win, the information on how they one gets processed and they try to attempt it again using that information!

Rather then focusing on attacking, these AI naturally plays offensively! You will see them defend their base while at the same time try to attack the enemy! The AI also doesn't know which spaces it must fill to win so as it plays it must learn on it's own (this also allows for the creation of custom maps).

iBlock has multiple different game options for how to set up the way the AI will play! New gamemodes coming soon!

Copyright (c) SavSec 2017

Copyright (c) SavSec iBlock 2017

Format:

	Encoding: UTF-8
	Tab: 2
	System: Python 2.7.11

Modules:

	sys, time, random

License:
	
	MIT License

Developer:
	
	@Russian_Otter - Instagram


# Main Dynamics #
iBlock's Training will be it making random moves. Unknown to iBlock: a certain set of spaces will be required inorder to win. Once random moves fill up the required spaces iBlock will note down the spaces that it owned.
Reoccuring spaces will remain in the player's memory file while spaces that didnt appear twice will be removed. Overtime iBlock will be able to point out which blocks it should capture if they are available.

~~The A* Algorithm will be applied while traveling far distances to reach a common point! The last point will always be regaurded as a winning space.~~

# Game Map Challanges #
This game can be customized so that the map can have different winning spaces that the AI must find!
Other options may involve changing the map every game to a list of preset maps and having AI find patterns!

# Players #
~~In the game's current direction, the game may only be iBlock vs iBlock. The game map isnt really human friendly...~~

iBlock can be both a game you watch and a game you play! Now with options for Bot vs Bot and Player vs Bot! The game will also log down how you play and where you like to move ~~(Don't worry though, the enemy bot does not observe how you play... yet)~~

# iBlock v2 (Current Stage) #
While looking through the code after seeing that during a reset, player 1 still was loosing games, it was discovered that an error in the code made it so player 1 was unable to learn. Along with this, the `last_move` variable was not working properly, which is now fixed. Both players are now more intelligent than they were before! The fitness levels of both bots have increased a lot and their ability to overcome a strong enemy has also appeared! There are still more learning technequies which need to be added (based on statistics) inorder to beat a human. iBlock will be able to beat human players in future updates.

Change Log:

	Player 1's Mental illness is fixed.
	
	Both players can process information more clearly
	
	New Rule: You can't undo the last 2 moves (can be modified)
	
	Human vs AI Mode
	
	Human movement data can be observed and be used/modified by the AI
	
	Arguments for game modes have been added


# iBlock v3 (Current Ideas) #
iBlock v3 will have options which will allow for a loosing bot to change up their plan of attack based on information that it gathers and moniters naturally. iBlock v3 will also have long term memory which it can use to help predict a human's patterns and decide which moves it should take to counter act the human.
(Memory clusters which contain multiple of the same spaces will increase the chances that predicted move will be choosen)
2-4 person death match mode will be added (dynamic coding required).
The board might be 10x10 to 20x20.

# iBlock v4 #
iBlock will observe you and will know how to defeat you......
