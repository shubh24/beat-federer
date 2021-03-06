from __future__ import division
import random
import matplotlib.pyplot as plt

class Player():
	def __init__(self, name, sets_won, games_won, points_won):
		self.name = name
		self.sets_won = sets_won
		self.games_won = games_won
		self.points_won = points_won

class Match():

	def __init__(self, me, fed):
		self.set_1 = "-1"  
		self.set_2 = "-1"  
		self.set_3 = "-1"  
		self.set_4 = "-1"  
		self.set_5 = "-1"
		self.set_count = me.sets_won + fed.sets_won + 1
		self.server = 0  #Federer's Service
		self.toggle = [1, 0]

		# fed_serve = 0.677*0.735 + 0.333*0.54
		self.fed_serve = 0.99 + 0.01*(0.772 - 0.5)/.5  
		# fed_return = 0.335
		self.fed_return = 0.99 - 0.01*(0.5 - 0.335/0.5)


	def play_point(self, me, fed, server):

		ran = random.random()

		if server == 0:
			if ran <= self.fed_serve:
				return fed
			else:
				return me
		else:
			if ran <= self.fed_return:
				return fed
			else:
				return me

	def play_tiebreak(self, me, fed):
		# me.points_won = 6
		# fed.points_won = 0
		while(max(me.points_won, fed.points_won) < 7):
			if (me.points_won + fed.points_won)%2 == 1:
				self.server = self.toggle[self.server] #Toggle server

			if me.points_won == 5 and fed.points_won == 5:		
				while(abs(me.points_won - fed.points_won) != 2):
					diffof2_winner = self.play_point(me, fed, self.server)
					diffof2_winner.points_won += 1				

					if (me.points_won + fed.points_won)%2 == 1:
						self.server = self.toggle[self.server] #Toggle server

				return me if me.points_won > fed.points_won else fed
			else:
				winner = self.play_point(me, fed, self.server)
				winner.points_won += 1
		
		return me if me.points_won > fed.points_won else fed 

	def play_game(self, me, fed):
		while(max(me.points_won, fed.points_won) < 4):
			if me.points_won == 3 and fed.points_won == 3:
				while(abs(me.points_won - fed.points_won) != 2):
					diffof2_winner = self.play_point(me, fed, self.server)
					diffof2_winner.points_won += 1							
			else:
				winner = self.play_point(me, fed, self.server)
				winner.points_won += 1

		self.server = self.toggle[self.server] #Toggle server
		return me if me.points_won > fed.points_won else fed 

	def play_set(self, me, fed):
		while(max(me.games_won, fed.games_won) < 6):
			
			if self.set_count != 5:			
				if me.games_won == 5 and fed.games_won == 5:
					fiveall_winner = self.play_game(me, fed)
					fiveall_winner.games_won += 1

					six5_winner = self.play_game(me, fed)
					six5_winner.games_won += 1

					if six5_winner.games_won == 7:
						return six5_winner
					
					elif six5_winner.games_won == 6:
						tiebreak_winner = self.play_tiebreak(me, fed)
						tiebreak_winner.games_won += 1
						return tiebreak_winner
			
			elif self.set_count == 5:
				if me.games_won >= 5 and fed.games_won >= 5:
					while(abs(me.games_won - fed.games_won) != 2):
						diffof2_winner = self.play_game(me, fed)
						diffof2_winner.games_won += 1
					return me if me.games_won > fed.games_won else fed

			winner = self.play_game(me, fed)
			winner.games_won += 1
			fed.points_won = 0
			me.points_won = 0

		if me.games_won + fed.games_won == 11:
			winner = self.play_game(me, fed)
			winner.games_won += 1

		if me.games_won == 6 and fed.games_won == 6:
			winner = self.play_tiebreak(me, fed)
			winner.games_won += 1

		return me if me.games_won > fed.games_won else fed 

	def play_match(self, me, fed):
		while(max(me.sets_won, fed.sets_won) < 3):
			winner = self.play_set(me, fed)
			winner.sets_won += 1

			var = "set_%s"%self.set_count
			self.__dict__[var] = "%s-%s"%(me.games_won, fed.games_won)
			self.set_count += 1
			me.games_won = 0
			fed.games_won = 0
			me.points_won = 0
			fed.points_won = 0

		# if me.sets_won > fed.sets_won:
		# 	print self.set_1, self.set_2, self.set_3, self.set_4, self.set_5
		return fed if fed.sets_won > me.sets_won else me

if __name__ == '__main__':

	arr = []
	starting_scores = []
	t_arr = []
	temp = 0
	for sets in range(2, 3, 1):
		for games in range(0,6,1):
			for points in range(0, 4, 1):				
				count = 0
				for iter in range(10000):
					fed = Player("federer", 0, 0, 0)
					me = Player("shubhankar", sets, games, points)
					winner = Match(me, fed).play_match(me, fed)
					if winner == me:
						count += 1
				t_arr.append(temp)
				temp += 1
				arr.append(float(count/10000))
				starting_scores.append(str((sets,games,points)))

	for points_me in range(0, 7, 1):
		count = 0
		for iter in range(10000):
			fed = Player("federer", 0, 6, 0)
			me = Player("shubhankar", 2, 6, points_me)
			winner = Match(me, fed).play_match(me, fed)
			if winner == me:
				count += 1
		t_arr.append(temp)
		temp += 1
		arr.append(float(count/10000))
		starting_scores.append(str((2,6,points_me)))


	plt.plot(arr)
	plt.xticks(t_arr, starting_scores, rotation = 30)
	plt.xlabel("My Starting Score, Format ==> (Sets, Games, Points)")
	plt.ylabel("Probability of win (as per simulation)")
	plt.show()

	# me = Player("shubhankar", 2, 1, 3)
	# winner = Match(me, fed).play_match(me, fed)
