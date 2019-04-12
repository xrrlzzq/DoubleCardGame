# DoubleCardGame
python version 3.63
run command : python boardDisplay.py( you should run this program in boardDisplay.py file)
In order to run correctly, you must put boardDisplay.py, gameBoard.py, ValidRule.py ,Helper.py, gameTree.py, MiniMax.py and cards.pnp in the same file

human mode:
step 1: run BoardDisplay.py
step 2: choose one role(color player or dot player), default is color player and click "start game" button
step3: enter your command in the command input box and then click move

if you want to batch move(copy a set of command and move ), then you need to paste the set of commands in the text box above the "bat move" button and then click "bat move" button

if you want to play the game again, then you need to click "stop game" button first and then back to step 2

if you want to quit the game, then you can click "quit" button

note: if the command is invalid or illegal ,there are error message to remind you and all of command history would show on the right side text box

AI mode:
step 1: before start game, you can choose if use auto mode or not ( if you choose auto mode, then AI can play automatically ) 
step 2: if you choose auto mode, then you can choose if AI playe first
step 3: you can choose if use alpha-beta puring or not and if generate trace file or not( alpha-beta puring would generate traceab.txt, otherwise would generate tracemm.txt, all of the file would be generated in the same file as boardDisplay.py)

AI check button can be used to AI funtion by manual 
note: this program temporarily only support naive heuristic  
