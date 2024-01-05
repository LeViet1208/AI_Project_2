For testing, run the main.py and enter the name of test file in test folder.
After running the program also return a output.txt contain score and the list of agent action, every action have form below:
	[t, [x, y]] 
	- t = 1 => Agent move to x, y
	- t = 2 => Agent shoot to x, y
	- t = 3 => Agent take gold in x, y
	- t = 4 => Killed Wumpus in x, y
	- t = 5 => Escape ([x, y] always [0, 0])
	- t = 6 => Dead in x, y 