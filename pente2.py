import random

def main():
	board = initializeBoard()
	currentTurnTokenColor = random.choice(["R", "B"])
	printBoard(board)
	board = generateRandomBoard(board, currentTurnTokenColor, 150)
	for i in range(5):
		print(" ")
	printBoard(board)
	checkForOpenThrees(board, currentTurnTokenColor)
	switchTurns(currentTurnTokenColor)
	checkForOpenThrees(board, currentTurnTokenColor)
	switchTurns(currentTurnTokenColor)

def initializeBoard():
	board = []
	for row in range(19):
		board.append([])
		for col in range(19):
			board[row].append(".")
	return board

def printBoard(board):
	for row in range(19):
		print("")
		for col in range(19):
			print(board[row][col] + "   ", end="")
		print(" ")

def switchTurns(currentTurnTokenColor):
	if currentTurnTokenColor == "R":
		return "B"
	else:
		return "R"

def generateRandomBoard(board, currentTurnTokenColor, numberOfTurns):
	for _ in range(numberOfTurns):
		validSpot = False
		while validSpot == False:
			xcord = random.randint(0, 18)
			ycord = random.randint(0, 18)
			validSpot = isValidSpot(xcord, ycord, board)
		board[ycord][xcord] = currentTurnTokenColor
		currentTurnTokenColor = switchTurns(currentTurnTokenColor)
	return board



main()
