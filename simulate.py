import random

class Player():
	def __init__(self, name):
		self.name = name
		self.sets_won = 0
		self.games_won = 0
		self.points_won = 0

class Match():

	def __init__(self):
		self.set_1 = "-1"  
		self.set_2 = "-1"  
		self.set_3 = "-1"  
		self.set_4 = "-1"  
		self.set_5 = "-1"
		self.set_count = 1
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
				print "yay"
				return me
		else:
			if ran <= self.fed_return:
				return fed
			else:
				print "yay"
				return me

	def play_tiebreak(self, me, fed):
		me.points_won = 0
		fed.points_won = 0
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
		me.points_won = 0
		fed.points_won = 0

		while(max(me.points_won, fed.points_won) < 4):
			if me.points_won == 3 and fed.points_won == 3:
				deuce_winner = self.play_point(me, fed, self.server)
				ad_winner = self.play_point(me, fed, self.server)
				if deuce_winner.name == ad_winner.name:
					ad_winner.points_won += 1					
			else:
				winner = self.play_point(me, fed, self.server)
				winner.points_won += 1

		self.server = self.toggle[self.server] #Toggle server
		return me if me.points_won > fed.points_won else fed 

	def play_set(self, me, fed):
		me.games_won = 0
		fed.games_won = 0
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
				if me.games_won == 5 and fed.games_won == 5:
					while(abs(me.games_won - fed.games_won) != 2):
						diffof2_winner = self.play_game(me, fed)
						diffof2_winner.games_won += 1
					return me if me.games_won > fed.games_won else fed

			winner = self.play_game(me, fed)
			winner.games_won += 1

		return me if me.games_won > fed.games_won else fed 

	def play_match(self, me, fed):
		while(max(me.sets_won, fed.sets_won) < 3):
			winner = self.play_set(me, fed)
			winner.sets_won += 1

			var = "set_%s"%self.set_count
			self.__dict__[var] = "%s-%s"%(me.games_won, fed.games_won)
			self.set_count += 1

		print self.set_1, self.set_2, self.set_3, self.set_4, self.set_5

if __name__ == '__main__':
	me = Player("shubhankar")
	fed = Player("federer")

	Match().play_match(me, fed)