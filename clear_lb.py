from pickle import *
f = open("player.txt","wb")
leaderboard = {}

dump(leaderboard, f)