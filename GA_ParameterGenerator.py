from Candidate import *
import math

TestCaseNum = '1a'
Popln_Size = 100
Max_Generations = 500
Mutation_percent = 5
Num_Games = 5			# to compute fitness for each candidate
Max_Moves = 200			# to compute fitness for each candidate
N_percent = 30			# for delete-n-last replacement. n will be N_percent of Popln_Size
Selection = 'TS' 		# TS: Tournament selection, RW: Roulette wheel
Crossover = 'Cross1'	# [a1, b1, c1, d1] X [a2, b2, c2, d2] = ([a1, b1, c1, d1] * fitness1) + ([a2, b2, c2, d2] * fitness2)
Max_Fitness = Num_Games * Max_Moves * 4 / 10


def writeExpParams(file):
	file.write("--------------------------------------------------------------------\n")
	file.write("TestCaseNum: " + str(TestCaseNum) + "\n")
	file.write("Popln_Size: " + str(Popln_Size) + "\n")
	file.write("Max_Generations: " + str(Max_Generations) + "\n")
	file.write("Mutation_percent: " + str(Mutation_percent) + "\n")
	file.write("Num_Games: " + str(Num_Games) + "\n")
	file.write("Max_Moves: " + str(Max_Moves) + "\n")
	file.write("N_percent: " + str(N_percent) + "\n")
	file.write("Selection: " + Selection + "\n")
	file.write("Crossover: " + Crossover + "\n")
	file.write("--------------------------------------------------------------------\n\n")


def printExpParams():
	print("--------------------------------------------------------------------")
	print("TestCaseNum: " + str(TestCaseNum))
	print("Popln_Size: " + str(Popln_Size))
	print("Max_Generations: " + str(Max_Generations))
	print("Mutation_percent: " + str(Mutation_percent))
	print("Num_Games: " + str(Num_Games))
	print("Max_Moves: " + str(Max_Moves))
	print("N_percent: " + str(N_percent))
	print("Selection: " + Selection)
	print("Crossover: " + Crossover)
	print("--------------------------------------------------------------------\n")


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


	def rouletteWheelSelection(self):
		# sum of fitnesses of all individuals in population
		sumFitness = np.sum(x.get_fitness() for x in self.population)

		# random number 0 <= r < 1
		rand = random.uniform(0, 1)

		partSum = 0
		for ind in self.population:
			prob_ind = ind.get_fitness()/sumFitness
			partSum += prob_ind
			if rand < partSum:
				return ind


	def deleteNLastReplacement(self, N_offsprings):
		N = len(N_offsprings)
		self.population = self.population[0:-N] + N_offsprings


	def generateNewPopulation(self):	
		offsprings = []
		N = (N_percent / 100) * Popln_Size
		num_offsprings = 0

		# Repeat until we have N offsprings
		while num_offsprings < N:
			# Select parents via specified selection mech.
			if Selection == 'RW':
				parent1 = self.rouletteWheelSelection()
				parent2 = self.rouletteWheelSelection()
			else: # 'TS'
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
		results_filename = "testCase" + TestCaseNum + ".txt"
		f = open(results_filename, 'w')
		writeExpParams(f)

		numGen = 0
		f.write("Gen no.\tAvgFit\tBestCandidate\tBestFitness\n")
		self.recordResults(f, numGen)

		while (numGen < Max_Generations and self.getAvgFitness() < Max_Fitness):
			self.generateNewPopulation()
			
			numGen += 1
			self.recordResults(f, numGen)

		f.close()


	def recordResults(self, file, numGen):
		# Write to file
		file.write(str(numGen) + "\t" \
			+ str(self.getAvgFitness()) + "\t"  \
			+ str(self.population[0]) + "\t"  \
			+ str(self.population[0].get_fitness()) + "\n")
		# Print to stdout
		print("Gen:", numGen, "AvgFitness:", self.getAvgFitness(), \
			"BestCandidate:", self.population[0], \
			"(fitness:", self.population[0].get_fitness(), ")")
		if Popln_Size <= 20:
			self.printPopln()


printExpParams()
test1 = GA_ParametersGenerator()
test1.GA_Tuner()
