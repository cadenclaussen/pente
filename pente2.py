import random

def main():
	board = initializeBoard()
	token = random.choice(["R", "B"])
	printBoard(board)
	board = generateRandomBoard(board, token, 150)
	for i in range(5):
		print(" ")
	printBoard(board)
	checkSituations(board, token)


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

def switchTurns(token):
	if token == "R":
		return "B"
	else:
		return "R"

def generateRandomBoard(board, token, numberOfTurns):
	for _ in range(numberOfTurns):
		validSpot = False
		while validSpot == False:
			xcord = random.randint(0, 18)
			ycord = random.randint(0, 18)
			validSpot = isValidSpot(xcord, ycord, board)
		board[ycord][xcord] = token
		token = switchTurns(token)
	return board

def checkSituations(board, token):
	patterns = []
	for row in range(0, 18):
		for col in range(0, 18):
			verify(board, row, col, [1, 0], token, ["open", "token", "token", "token", "open"], "open three", patterns)
			# verify(board, row, col, [1, 0], token, ["closed", "token", "token", "token", "token", "open"], "closed four", patterns)

def verify(board, row, col, deltas, token, pattern, typeOfPattern, patterns):
	for patternIndex in range(len(pattern)):
		isBeadAtSpot = isBead(board, row, col, token, pattern[patternIndex - 1])

def isBead(board, row, col, token, tokenType):

	if row > 18:
		return False
	if row < 0:
		return False
	if col > 18:
		return False
	if col < 0:
		return False

	if board[row][col] == token and "token" == tokenType:
		return True

	if token == "R":
		oposingToken = "B"
	else:
		oposingToken = "R"

	if board[row][col] == oposingToken and "closed" == tokenType:
		return True

	if board[row][col] == "." and "open" == tokenType:
		return True

	print("Error")


main()
