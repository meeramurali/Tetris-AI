from Candidate import *
import math

Popln_Size = 20
Max_Generations = 1000
Mutation_percent = 5
Num_Games = 2		# to compute fitness for each candidate
Max_Moves = 200		# to compute fitness for each candidate
N_percent = 30		# for delete-n-last replacement. n will be N_percent of Popln_Size
Max_Fitness = Num_Games * Max_Moves * 4 / 10


class GA_ParametersGenerator:

	def __init__(self):
		self.population = self.initPopulation()
		self.population = self.sortCandidatesByFitness(self.population)
		self.avg_fitness = self.getAvgFitness()


	def initPopulation(self):
		popln = []
		for i in range(Popln_Size):
			popln.append(Candidate(num_games=Num_Games, max_moves=Max_Moves))
		return popln


	def printPopln(self):
		print("---------------------")
		for each in self.population:
			print(each, "(fitness", each.get_fitness(), ")")
		print("---------------------")


	def sortCandidatesByFitness(self, candidates):
		return sorted(candidates, key=lambda x: x.get_fitness(), reverse=True)


	def getAvgFitness(self):
		sumFitness = 0
		for x in self.population:
			sumFitness += x.get_fitness()

		return sumFitness / Popln_Size 


	def tournamentSelection(self):
		# Randomly sample 10% of the population
		size_10percent = math.floor((10 / 100) * Popln_Size)
		sample_10percent_indices = np.random.randint(0, Popln_Size, size_10percent)

		# Population assumed to be pre-sorted by fitness
		# So to pick best 2 candidates from the 10% sample, just pick smallest 2 indices
		sample_10percent_indices = sorted(sample_10percent_indices)
		best1 = sample_10percent_indices[0]

		if len(sample_10percent_indices) > 1:
			best2 = sample_10percent_indices[1]
			return self.population[best1], self.population[best2]

		return self.population[best1]


	def deleteNLastReplacement(self, N_offsprings):
		N = len(N_offsprings)
		self.population = self.population[0:-N] + N_offsprings


	def generateNewPopulation(self):	
		offsprings = []
		N = (N_percent / 100) * Popln_Size
		num_offsprings = 0

		# Repeat until we have N offsprings
		while num_offsprings < N:
			# Select parents via tournament selection
			parent1, parent2 = self.tournamentSelection()

			# Create offspring via crossover
			offspring = Candidate(parent1.crossover(parent2), num_games=Num_Games, max_moves=Max_Moves)

			# Mutate if required
			if (random.random() < (Mutation_percent / 100)):
				print("Mutation!")
				offspring.mutate()

			# print("parent1", parent1)
			# print("parent2", parent2)
			# print("offspring", offspring)

			offsprings.append(offspring)
			num_offsprings += 1

		# Replace N weakest candidates from the population with offsprings
		self.deleteNLastReplacement(offsprings)

		# Sort new population by fitness
		self.population = self.sortCandidatesByFitness(self.population)


	def GA_Tuner(self):
		numGen = 0
		avg_fitness = self.getAvgFitness()

		print("Gen:", numGen, "AvgFitness:", self.getAvgFitness())
		if Popln_Size <= 20:
			self.printPopln()

		while (numGen < Max_Generations and avg_fitness < Max_Fitness):
			self.generateNewPopulation()
			numGen += 1
			print("Gen:", numGen, "AvgFitness:", self.getAvgFitness())
			if Popln_Size <= 20:
				self.printPopln()


test1 = GA_ParametersGenerator()
test1.GA_Tuner()
