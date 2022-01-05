import random
import sys

def main():
	board = initializeBoard()
	token = random.choice(["R", "B"])
	printBoard(board)
	board = generateRandomBoard(board, token, 200)
	for i in range(5):
		print(" ")
	printBoard(board)
	isPatterns(board, "R")
	isPatterns(board, "B")


def initializeBoard():
	board = []
	for row in range(19):
		board.append([])
		for col in range(19):
			board[row].append(".")
	return board

def printBoard(board):
	print("   ", end="")
	for col in range(19):
		print(str(col  % 10) + "   ", end="")
	print()
	for row in range(19):
		print(str(row % 10)  + "  ", end="")
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

def generateCreatedBoard(board, token, numberOfTurns):
	board[1][1] = 'B'
	board[1][2] = "R"
	board[1][3] = "R"
	board[1][4] = "R"
	board[1][5] = "R"
	return board

def isValidSpot(xcord, ycord, board):
	if board[xcord][ycord] == ".":
		return True
	else:
		return False


def isPatterns(board, token):
	patternsFound = []
	openThree = { "name": "Open Three", "tokens": [ "open", "token", "token", "token", "open" ] }
	openFour = { "name": "Open Four", "tokens": [ "open", "token", "token", "token", "token", "open" ] }
	holedOpenFourOne = { "name": "Holed Open Four", "tokens": [ "open", "token", "open", "token", "token", "open" ] }
	holedOpenFourTwo = { "name": "Holed Open Four", "tokens": [ "open", "token", "token", "open", "token", "open" ] }
	five = { "name": "Five - Won", "tokens": [ "token", "token", "token", "token", "token" ] }
	closedFourOne = { "name": "Closed Four", "tokens": [ "token", "token", "token", "token", "closed", "open" ] }
	closedFourTwo = { "name": "Closed Four", "tokens": [ "closed", "token", "token", "token", "token", "open" ] }
	holedFiveOne =  { "name": "Holed Five", "tokens": [ "open", "token", "token", "token", "open", "token" ] }
	holedFiveTwo = { "name": "Holed Five", "tokens": [ "token", "open", "token", "token", "token", "open" ] }
	holedFiveThree = { "name": "Holed Five", "tokens": [ "open", "token", "token", "open", "token", "token", "open" ] }
	patterns = [ openThree, openFour, holedOpenFourOne, holedOpenFourTwo, five, closedFourOne, closedFourTwo, holedFiveOne, holedFiveTwo, holedFiveThree  ]
	for pattern in patterns:
		isPattern(board, token, pattern, patternsFound)
	return patternsFound


def isPattern(board, token, pattern, patternsFound):
	for row in range(0, 18):
		for col in range(0, 18):
			position = {"row": row, "col": col}
			isPatternAtPosition(board, token, pattern, position, patternsFound)

def isPatternAtPosition(board, token, pattern, position, patternsFound):
	directions = [ { "name": "East", "rowDelta": 0, "colDelta": 1 }, { "name": "South-East", "rowDelta": 1, "colDelta": 1 }, { "name": "South", "rowDelta": 1, "colDelta": 0 }, { "name": "South-West", "rowDelta": 1, "colDelta": -1 } ]
	for direction in directions:
		found = isPatternAtPositionInDirection(board, token, pattern, position, direction)
		if found:
			patternsFound.append({"name": "open three", "direction": direction["name"], "position": position})
			print(pattern["name"] + " detected. Direction - " + direction["name"] + ". Color - " + token + ". Position - " + str(position["row"]) + ", " + str(position["col"]))
			if pattern["name"] == "Five - Won":
				print(token + " won!")
				sys.exit()
			
# board: 19x19 array
# position: dictionary with row, col
# pattern: dictionary with name and tokens [ 'closed', 'token', 'token' ...]
# direction: dictionary with name, rowDelta, colDelta
# token: current players token color, eg 'R'
def isPatternAtPositionInDirection(board, token, pattern, position, direction):
	isBeadAtSpot = False
	for expectedToken in pattern["tokens"]:
		isBeadAtSpot = isToken(board, token, position, expectedToken)
		if isBeadAtSpot == True:
			position = {  "row": (position["row"] + direction["rowDelta"]), "col": (position["col"] + direction["colDelta"])}
		if isBeadAtSpot == False:
			return False

	return True

# board: 19x19 array
# position: dictionary with row, col
# token: current players token color, eg 'R'
def isToken(board, token, position, expectedToken):
	row = position["row"]
	col = position["col"]

	if expectedToken == "closed" and (row > 18 or row < 0 or col > 18 or col < 0):
		return True


	if row > 18:
		return False
	if row < 0:
		return False
	if col > 18:
		return False
	if col < 0:
		return False

	if board[row][col] == token and expectedToken == "token":
		return True

	if token == "R":
		oposingToken = "B"
	if token == "B":
		oposingToken = "R"

	if board[row][col] == oposingToken and expectedToken == "closed":
		return True

	if board[row][col] == "." and expectedToken == "open":
		return True

	return False



main()
