from Piece import *

class Random_Piece_Generator:

    def __init__(self):
        self.bag = np.arange(7)
        self.shuffleBag()
        self.index = -1


    def nextPiece(self):
        self.index += 1
        if self.index >= len(self.bag):
            self.shuffleBag()
            self.index = 0

        return Piece().select_piece(self.bag[self.index])


    def shuffleBag(self):
        np.random.shuffle(self.bag)


# test = Random_Piece_Generator()
# print(test.bag)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
# print(test.nextPiece().cells)
