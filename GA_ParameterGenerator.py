from AI_Player import *
from Random_Piece_Generator import *
import math
import random
import collections
class Tuner:

    def __init__(self):
            self.candidate = {"heightWeight": random.random() - 0.5,
                              "linesWeight" : random.random() - 0.5,
                              "holesWeight" : random.random() - 0.5,
                              "bumpinessWeight" : random.random() - 0.5 }


    def randomInteger(self,min,max):
        return random.random() * (max-min) + min
    
    def normalize(self,**candidate):
        norm = math.sqrt(candidate['heightWeight'] * candidate['heightWeight'] + candidate['linesWeight'] * candidate['linesWeight'] +
                         candidate['holesWeight'] * candidate['holesWeight'] + candidate['bumpinessWeight']*candidate['bumpinessWeight'] )
        print(norm)
        candidate['heightWeight'] /= norm
        candidate['linesWeight']= norm
        candidate['holesWeight'] /= norm
        candidate['bumpinessWeight'] /= norm
        print(candidate)

    def generateRandomcandidate(self):
        candidate = {'heightWeight': random.random() - 0.5,
                     'linesWeight' : random.random() - 0.5,
                     'holesWeight': random.random() - 0.5,
                     'bumpinessWeight' : random.random() - 0.5 }
        print(candidate)
        self.normalize(**candidate)

        return candidate
    
    def candidateSort(self,candidates):
        #sorted_x = [int(v) for k,v  in candidates[0].items()]
        self.candidates = sorted(candidates, key=lambda kv: (kv['bumpinessWeight'],kv['holesWeight'],kv['linesWeight'],kv['heightWeight']),reverse=True)

    def computeFitness(self,candidates, numberOfGames, maxNumberOfMoves):

        for i in range(len(candidates)):
            self.candidate = candidates[i]
            self.ai = AI_Player(self.candidate['heightWeight'], self.candidate['linesWeight'], self.candidate['holesWeight'], self.candidate['bumpinessWeight'])
            self.totalScore = 0
            for j in range(numberOfGames) :
                self.grid = Board(22,10)
                rpg = Random_Piece_Generator()
                self.workingPieces = [rpg.nextPiece(),rpg.nextPiece()]
                self.workingPiece = self.workingPieces[0]
                self.score = 0
                numberOfMoves = 0
                numberOfMoves += 1
                while (numberOfMoves < maxNumberOfMoves) and not self.grid.isFull():
                   self.workingPiece = self.ai.select_move(self.grid, self.workingPieces)
                   reached_end = False
                   while not reached_end and self.workingPiece is not None:
                       if not self.workingPiece.moveDown(self.grid):
                           reached_end = True
                   if self.workingPiece is not None:
                       self.grid.addPiece(self.workingPiece)
                   self.score += self.grid.clearLines()
                   for k in range(len(self.workingPieces)-1):
                    self.workingPieces[k] = self.workingPieces[k+1]
                   self.workingPieces[len(self.workingPieces)-1] = rpg.nextPiece()
                   self.workingPiece = self.workingPieces[0]
                self.totalScore += self.score
                print(self.totalScore)
            fitness = self.totalScore

    def tournamentselectPair(self,candidates,ways):
        indices = []
        for i in range(len(candidates)):
            indices.append(i)
        fittestCandidateIndex1 = None
        fittestCandidateIndex2 = None
        for i in range(ways):
            splicenum = math.floor(self.randomInteger(0,len(indices)))
            print('splicenum is ', splicenum)
            selectedIndex = indices[splicenum:1]
            print(selectedIndex)
            if(fittestCandidateIndex1 == None or selectedIndex[0] < fittestCandidateIndex1 ):
                fittestCandidateIndex2 = fittestCandidateIndex1
                fittestCandidateIndex1 = selectedIndex[0]
            elif(fittestCandidateIndex2 == None or selectedIndex[0] < fittestCandidateIndex2):
                fittestCandidateIndex2 = selectedIndex[0]
        print(fittestCandidateIndex1)
        print(fittestCandidateIndex2)
        return[candidates[fittestCandidateIndex1],candidates[fittestCandidateIndex2]]

    def crossOver(self,candidate1,candidate2):
        candidate = { "heightWeight": candidate1.fitness * candidate1.heightWeight + candidate2.fitness * candidate2.heightWeight,
                      "linesWeight": candidate1.fitness * candidate1.linesWeight + candidate2.fitness * candidate2.linesWeight,
                      "holesWeight": candidate1.fitness * candidate1.holesWeight + candidate2.fitness * candidate2.holesWeight,
                      "bumpinessWeight": candidate1.fitness * candidate1.bumpinessWeight + candidate2.fitness * candidate2.bumpinessWeight
        }                    
        normalize(candidate)
        return candidate
    
    def mutate(self,candidate):
        quantity = random.randint() * 0.4 - 0.2
        
        mutateelement = self.randomInteger(0,4)

        if(mutateelement ==0):
            candidate.heightWeight += quantity
        elif(mutateelement == 1):
            candidate.linesWeight += quantity
        elif(mutateelement == 2):
            candidate.holesWeight += quantity
        elif(mutateelement == 3):
            candidate.bumpinessWeight += quantity

   # def deleteNLastReplacement(self,candidates,newCandidates):
   #     candidates.splice(-len(newCandidates))
    #    for i in range(len(newCandidates)):
    #        candidates.append(newCandidates[i])
    #    candidateSort(candidates)
       

    def tune(self):
        self.candidates = []
        for i in range(2):
            self.candidates.append(self.generateRandomcandidate())
        print('computing the fitness of initial population')
        print(self.candidates)
        self.computeFitness(self.candidates,1,2)
        print(self.candidates)
        self.candidateSort(self.candidates)
        count = 0
        print('Initial fitness computed')
        while True:
            newCandidates = []
            for i in range(5):
                pair = self.tournamentselectPair(self.candidates,10)
                candidate = self.crossOver(pair[0],pair[1])
                if random.random() < 0.05:
                    self.mutate(candidate)
                normalize(self.candidate)
                newCandidates.append(candidate)
            print('Computing fitnesses of new candidates:', count)
            self.computeFitness(newCandidates,2,10)
            print('computed the fitness')
         #   deleteNLastReplacement(candidates,newCandidates)
            totalFitness = 0
            for i in range(len(self.candidates)):
                totalFitness += self.candidates[i].fitness
            print('Average Fitness', (totalFitness/len(self.candidates)))
           # print('Highest Fitness', candidates[0].fitness)
            count += 1


test1 = Tuner()
test1.tune()





