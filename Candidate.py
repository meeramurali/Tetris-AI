import random
import numpy as np
from TetrisAI import *


class Candidate:
	def __init__(self, params=None, num_games=100, max_moves=500):
		"""
		params[0] --> heightWt
		params[1] --> linesWt
		params[2] --> holesWt
		params[3] --> bumpinessWt

		"""
		if params is None:
			self.params = self.generateRandomParams()
		else:
			self.params = np.array(params, dtype=float)

		self.num_games = num_games
		self.max_moves = max_moves
		self.fitness = None		


	def __str__(self):
		return str(self.params)


	def get_fitness(self):
		# fitness = average score over specified number of games
		if self.fitness is None:
			total_score = 0
			for g in range(self.num_games):
				tetris = TetrisAI(self.params)
				tetris.run_trainMode(self.max_moves)
				total_score += tetris.score

			self.fitness = total_score / self.num_games

		return self.fitness


	def generateRandomParams(self):
		params = np.random.uniform(-1, 1, 4)
		params = self.normalize(params)
		return params


	def normalize(self, params):
		norm = np.linalg.norm(params)
		if norm == 0: 
		   return params
		return params / norm	


	def mutate(self):
		# Add random amount between -0.2 to 0.2 to a random parameter
		mutation_amt = random.uniform(-0.2, 0.2)
		mutation_loc = random.randint(0, 3)
		self.params[mutation_loc] += mutation_amt
			

	def crossover(self, other):
		child_params = self.params * self.get_fitness() + other.params * other.get_fitness()
		child_params = self.normalize(child_params)
		return child_params



# test = Candidate()
# print(test)
# test = Candidate([-1, 2, -3, -4], 3)

# test2 = Candidate([-2, 4, -5, -6], 3)
# print(test.get_fitness(), test2.get_fitness())
# print(test.crossover(test2))

# print(test)
# test.mutate()
# print(test)

# test3 = Candidate(num_games=10, max_moves=200)
# import time
# start = time.time()
# print(test3.get_fitness())
# end = time.time()
# print("Run time (min): ", (end - start)/60)


