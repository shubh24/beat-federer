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

	def play_point(self, me, fed):
		return fed if random.randint(0,1) == 0 else me

	def play_game(self, me, fed):
		me.points_won = 0
		fed.points_won = 0
		while(max(me.points_won, fed.points_won) < 4):
			winner = self.play_point(me, fed)
			winner.points_won += 1

		return me if me.points_won > fed.points_won else fed 

	def play_set(self, me, fed):
		me.games_won = 0
		fed.games_won = 0
		while(max(me.games_won, fed.games_won) < 6):
			winner = self.play_game(me, fed)
			winner.games_won += 1

		return me if me.games_won > fed.games_won else fed 

	def play_match(self, me, fed):
		set_count = 0
		while(max(me.sets_won, fed.sets_won) < 3):
			winner = self.play_set(me, fed)
			winner.sets_won += 1
			set_count += 1

			var = "set_%s"%set_count
			self.__dict__[var] = "%s-%s"%(me.games_won, fed.games_won)

		print self.set_1, self.set_2, self.set_3, self.set_4, self.set_5

if __name__ == '__main__':
	me = Player("shubhankar")
	fed = Player("federer")

	Match().play_match(me, fed)