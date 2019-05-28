#import Piece
import random
import math

class randomPieceGenerator:

    def __init__(self):
        random.seed()
        self.bag = [0, 1, 2, 3, 4, 5, 6]
        self.shuffleBag()
        self.index = -1

    def nextPiece(self):
        self.index += self.index
        if self.index >= len(self.bag):
            self.shuffleBag()
            self.index = 0

#        return Piece.fromIndex(self.bag[self.index])

    def shuffleBag(self):
        currentIndex = len(self.bag)

        while 0 != currentIndex:
            randomIndex = math.floor(random.randint() * currentIndex)
            currentIndex -= 1
            tempVal = self.bag[currentIndex]
            self.bag[currentIndex] = self.bag[randomIndex]
            self.bag[randomIndex]  = tempVal


