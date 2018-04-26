class TicTacToe():
	def __init__(self):
		self.game = "000000000"
		self.turn = 0
		self.winner = False
		self.movesRemaining = 9
		self.playerWinner = -1

	def makeMove(self, player, pos):
		if (self.winner != False):
			raise ValueError("%s Game over." % self.winner)
		if (self.movesRemaining < 1):
			raise ValueError("No more moves remain.")
		if (self.turn != player):
			raise ValueError("Its not player %d's turn." % player)
		if pos > 8:
			raise ValueError('Position must be 0-8.')
		if (self.game[pos] != "0"):
			print("FATAL: Player %d" % self.turn)
			print("Move requested: %d" % pos)
			self.printState()
			raise ValueError('Position is already filled')

		moveType = "1"
		if self.turn == 1:
			moveType = "2"

		self.game = self.game[:pos] + moveType + self.game[pos +1:]
		self.movesRemaining -= 1
		self.turn = not self.turn
		return self.checkForWin()

	def printState(self):
		for i in range(len(self.game)):
			if self.game[i] == "0":
				print("|   |", end="")
			else:
				if self.game[i] == "1":
					char = "X"
				elif self.game[i] == "2":
					char = "O"
				print("| %s |" % char, end="")
			if ((i + 1) % 3) == 0:
				print("")

	def getFreeOptions(self):
		vals = []
		for i in range(0, len(self.game)):
			if self.game[i] == "0":
				vals.append(i)

		return vals

	def checkForWin(self):
		wins = [
			[0,1,2],
			[0,3,6],
			[2,5,8],
			[6,7,8],
			[0,4,8],
			[2,4,6],
			[1,4,7]
		]

		for pattern in wins:
			c = 0
			start = self.game[pattern[0]]
			for i in pattern:
				if self.game[i] == start and self.game[i] != "0":
					c += 1

			if c == 3:
				self.winner = "Player %d wins!" % (not self.turn)
				self.playerWinner = (not self.turn)
				#print("Winner! Player %d wins!" % (not self.turn))
				return True

		return False
