from random import randint
from game import TicTacToe

def generateGames():
	games = {}
	for i in range(0,(3**9)):
		c = i
		entry = ""
		stats = []
		for j in range(0,9):
			entry += str(int(c % 3))
			c /= 3
		for k in range(len(entry)):
			stats.append(0)
			if entry[k] == "0":
				stats[k] = 100
		games[entry] = {
			'entry': entry,
			'stats': stats
		}

	return games

def getPrediction(values):
	hstIdx = -1
	hst = 0
	for i in range(len(values['stats'])):
		if values['stats'][i] > hst:
			hst = values['stats'][i]
			hstIdx = i
	return hstIdx

def getUserMove(game):
	freeOpts = game.getFreeOptions()
	move = ""
	game.printState()
	while True:
		try:
			move = int(input("Enter move: 1-9: ")) -1
		except:
			print("Invalid entry")

		acc = False
		for i in freeOpts:
			if move == i:
				acc = True
				break

		if acc:
			break

	return move

# Random set of games.
bestAttempt = False
bestStats = [0, 999999]
bestLossStack = []
bestWinStack = []

for attempts in range(10):
	brain = generateGames()
	wonStats = [0, 0]
	lossStack = []
	winStack = []
	for n in range(20000):
		#print("Training against randomised player... %.2f%s" % (n / 1500 * 100, "%"))
		player = 0
		game = TicTacToe()
		moveStack = {}
		for i in range(9):
			freeOpts = game.getFreeOptions()
			move = freeOpts[randint(0, len(freeOpts) -1)]
			if player == 0:
				#Machine learn, on all except first iteration.
				if n > 0:
					move = getPrediction(brain[game.game])
					if move == -1:
						move = freeOpts[randint(0, len(freeOpts) -1)]
			moveStack[game.game] = move
			game.makeMove(player, move)
			player = not player
			if game.winner:
				break

		#game.printState()
		reward = 0

		# If draw, do nothing.
		if game.playerWinner == -1:
			continue

		wonStats[game.playerWinner] += 1
		if game.playerWinner == 0:
			# Machine won. Reward.
			reward = 1 * ((9 - i))
			#print(9 - i)s
		else:
			#Machine lost. Revoke.
			reward = -2 * ((9 -i))

		if n > 0:
			percentWon = (wonStats[0] / n) * 100
			winStack.append(percentWon)
			percentLost = 100 - (((n - wonStats[1]) / n) * 100)
			lossStack.append(percentLost)

		for key in moveStack:
			brain[key]['stats'][moveStack[key]] += reward

	print("Stats [machine learned wins, brain wins]")
	print(wonStats)

	if wonStats[1] < bestStats[1]:
		bestAttempt = brain
		bestStats = wonStats
		bestWinStack = winStack
		bestLossStack = lossStack

print("BEST:")
print("Stats [brain wins, brain losses]")
print(bestStats)
brain = bestAttempt

with open("stats.csv", "a") as fh:
	for i in range(len(bestLossStack)):
		if i % 10 == 0:
			fh.write(str(bestLossStack[i]) + "," + str(bestWinStack[i]) + "\n")

#quit()
print("Good luck!")
game = TicTacToe()
player = 0
for i in range(9):
	if player == 0:
		#Machine learn.
		move = getPrediction(brain[game.game])
		if move == -1:
			move = freeOpts[randint(0, len(freeOpts) -1)]
	else:
		#Get user move.
		move = getUserMove(game)

	game.makeMove(player, move)
	player = not player
	if game.winner:
		break

if game.playerWinner == -1:
	print("Draw!")
elif game.playerWinner == 0:
	print("Machine won!")
else:
	print("You won!")

game.printState()
