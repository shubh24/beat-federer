from __future__ import division
from simulate import *
import matplotlib.pyplot as plt

def win_game(p):
	return (pow(p,4)*(-8*pow(p,3) + 28*pow(p,2) - 34*p + 15))/(pow(p, 2) + pow(1-p, 2))

def win_tiebreak(p):
	q = 1 - p
	return pow(p, 7)*(1 + 7*q + 28*q*q + 84*pow(q, 3) + 210*pow(q, 4) + 462*pow(q, 5)) + 924*pow(p, 8)*pow(q, 6)/(1 - 2*p*q)

def win_set(p):
	w = win_game(p)
	z = 1 - w
	return (pow(w, 6) + 6*pow(w, 6)*z + 21*pow(w, 6)*pow(z, 2) + 56*pow(w, 6)*pow(z,3) + 126*pow(w, 6)*pow(z, 4) + 252*pow(w, 7)*pow(z, 5) + 504*pow(w,6)*pow(z,6)*win_tiebreak(p))

def win_match(p):
	s = win_set(p)
	q = 1 - s
	return (pow(s, 3) + 3*pow(s,3)*pow(q, 1) + 6*pow(s,3)*pow(q,2))

def third_set_five_love(me, fed, p):
	if fed.games_won < 7:
		fed.games_won += 1
		return  win_game(p) + (1-win_game(p))*(third_set_five_love(me, fed, p)) 
	else:
		return 0

def game_win_prob():
	arr = []
	win_game_probs = []
	for i in range(0, 100):
		arr.append(float(i/100))
		win_game_probs.append(win_game(float(i/100)))

	return plt.plot(arr, win_game_probs, label = "Win a game")

def set_win_prob():
	arr = []
	win_set_probs = []
	for i in range(0, 100):
		arr.append(float(i/100))
		win_set_probs.append(win_set(float(i/100)))

	return plt.plot(arr, win_set_probs, label = "Win a set")

def match_win_prob():
	arr = []
	win_match_probs = []
	for i in range(0, 100):
		arr.append(float(i/100))
		win_match_probs.append(win_match(float(i/100)))

	return plt.plot(arr, win_match_probs, label = "Win a match")

def plot():
	game_plot = game_win_prob()
	set_plot = set_win_prob()
	match_plot = match_win_prob()
	plt.legend(loc = "upper left")
	plt.xlabel("Probability of winning a point against Federer")
	plt.ylabel("Probability you'll...")
	plt.show()

if __name__ == '__main__':
	me = Player("shubhankar", 2, 5, 3)
	fed = Player("federer", 0, 0, 0)

	set_count = me.sets_won + fed.sets_won
	p = 0.01
	prob = 0

	prob = p + (1-p)*p + (1-p)*(1-p)*p + pow((1-p), 4)*third_set_five_love(me, fed, p) #WHEN going for 2 sets all, 5-0 in the third set
	prob += (1-prob)*win_set(p)
	print prob
	# plot()