class Board:
	def __init__(self, board):
		self.board = board
		

	def initialize(self):
		print("Initializing board")
		for row in range(19):
			self.board.append([])
			for col in range(19):
				self.board[row].append(".")
	return self.board

	def print(self):
		print("   ", end="")
		for col in range(19):
			print(str(col  % 10) + "   ", end="")
		print()
		for row in range(19):
			print(str(row % 10)  + "  ", end="")
			for col in range(19):
				print(str(self.board[row][col]) + "   ", end="")
			print(" ")

	def generateRandom(self, color, numberOfTurns):
		for _ in range(numberOfTurns):
			validSpot = False
			while validSpot == False:
				xcord = random.randint(0, 18)
				ycord = random.randint(0, 18)
				validSpot = isValidSpot(xcord, ycord, self.board)
			self.board[ycord][xcord] = color
			color = controller.switchTurns(color)
		return board

	def generateCreated(self):
		self.board[1][1] = 'B'
		self.board[1][2] = "R"
		self.board[1][3] = "R"
		self.board[1][4] = "R"
		self.board[1][5] = "R"
		return self.board

	def isValidSpot(self, xcord, ycord):
		if self.board[xcord][ycord] == ".":
			return True
		else:
			return False

	def isWinningPatterns(self, color):
		patternsFound = []
		five = { "name": "Five - Won", "tokens": [ "nonToken", "token", "token", "token", "token", "token", "nonToken" ] }
		six = { "name": "Six - Won", "tokens": [ "nonToken", "token", "token", "token", "token", "token", "token", "nonToken" ] }
		seven = { "name": "Seven - Won", "tokens": [ "nonToken", "token", "token", "token", "token", "token", "token", "token", "nonToken" ] }
		eight = { "name": "Eight - Won", "tokens": [ "nonToken", "token", "token", "token", "token", "token", "token", "token", "token", "nonToken" ] }
		nine = { "name": "Nine - Won", "tokens": [ "nonToken", "token", "token", "token", "token", "token", "token", "token", "token", "token", "nonToken" ] }
		jump = {"name": "jump", "tokens": [ "oposite", "token", "token", "oposite" ]}
		patterns  = [nine, eight, seven, six, five]
		for pattern in patterns:
			isPattern(self.board, color, pattern, patternsFound)
		return patternsFound

	def isCommonPatterns(self, color):
		patternsFound = []
		openThree = { "name": "Open Three", "tokens": [ "open", "token", "token", "token", "open" ] }
		openFour = { "name": "Open Four", "tokens": [ "open", "token", "token", "token", "token", "open" ] }
		holedOpenFourOne = { "name": "Holed Open Four", "tokens": [ "open", "token", "open", "token", "token", "open" ] }
		holedOpenFourTwo = { "name": "Holed Open Four", "tokens": [ "open", "token", "token", "open", "token", "open" ] }
		closedFourOne = { "name": "Closed Four", "tokens": [ "token", "token", "token", "token", "closed", "open" ] }
		closedFourTwo = { "name": "Closed Four", "tokens": [ "closed", "token", "token", "token", "token", "open" ] }
		holedFiveOne =  { "name": "Holed Five", "tokens": [ "open", "token", "token", "token", "open", "token" ] }
		holedFiveTwo = { "name": "Holed Five", "tokens": [ "token", "open", "token", "token", "token", "open" ] }
		holedFiveThree = { "name": "Holed Five", "tokens": [ "open", "token", "token", "open", "token", "token", "open" ] }
		patterns = [ openThree, openFour, holedOpenFourOne, holedOpenFourTwo, closedFourOne, closedFourTwo, holedFiveOne, holedFiveTwo, holedFiveThree  ]
		for pattern in patterns:
			isPattern(self.board, color, pattern, patternsFound)
		return patternsFound

	def isPattern(self, color, pattern, patternsFound):
		for row in range(0, 18):
			for col in range(0, 18):
				position = {"arow": row, "col": col}
				isPatternAtPosition(self.board, color, pattern, position, patternsFound)

	def isPatternAtPosition(self, color, pattern, position, patternsFound):
		directions = [ { "name": "East", "rowDelta": 0, "colDelta": 1 }, { "name": "South-East", "rowDelta": 1, "colDelta": 1 }, { "name": "South", "rowDelta": 1, "colDelta": 0 }, { "name": "South-West", "rowDelta": 1, "colDelta": -1 } ]
		for direction in directions:
			found = isPatternAtPositionInDirection(self.board, color, pattern, position, direction)
			if found:
				patternsFound.append({"name": pattern["name"], "direction": direction["name"], "position": position})
				print(pattern["name"] + " detected. Direction - " + direction["name"] + ". Color - " + color + ". Position - " + str(position["row"]) + ", " + str(position["col"]))
				if pattern["name"] == "jump":
					if color == "R":
						redJumps += 1
					if color == "B":
						blueJumps += 1

					if redJumps == 5:
						print("Red won!")
						sys.exit()
					if blueJumps == 5:
						print("Blue won!")
						sys.exit()

				if pattern["name"] == "Five - Won":
					print(colr + " won!")
					sys.exit()

	def isPatternAtPositionInDirection(self, color, pattern, position, direction):
		isBeadAtSpot = False
		for expectedToken in pattern["tokens"]:
			isBeadAtSpot = isToken(self.board, color, position, expectedToken)
			if isBeadAtSpot == True:
				position = {  "row": (position["row"] + direction["rowDelta"]), "col": (position["col"] + direction["colDelta"])}
			if isBeadAtSpot == False:
				return False

		return True

	def isToken(self, color, position, expectedToken):
		row = position["row"]
		col = position["col"]

		if expectedToken == "oposite":
			if color == "R":
				oposingToken = "B"
			if color == "B":
				oposingToken = "R"

			if self.board[row][col] == oposingToken:
				return True

		if expectedToken == "nonToken":
			if expectedToken == "closed" and (row > 18 or row < 0 or col > 18 or col < 0):
				return True

			if color == "R":
				oposingToken = "B"
			if color == "B":
				oposingToken = "R"

			if self.board[row][col] == oposingToken and expectedToken == "closed":
				return True

			if self.board[row][col] == "." and expectedToken == "open":
				return True


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

		if self.board[row][col] == color and expectedToken == "token":
			return True

		if color == 0:
			oposingToken = "B"
		if color == 1:
			oposingToken = "R"

		if self.board[row][col] == oposingToken and expectedToken == "closed":
			return True

		if self.board[row][col] == "." and expectedToken == "open":
			return True

		return False

board = []
boardO = Board(board)
board = boardO.initialize()