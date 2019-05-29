from Board import *
from Piece import *

class AI_Player:
	
	def __init__(self, heightWt, linesWt, holesWt, bumpinessWt):
		self.heightWt = heightWt
		self.linesWt = linesWt
		self.holesWt = holesWt
		self.bumpinessWt = bumpinessWt
		
	def get_best_move(self, board, workingPieces, currentPieceIndex):
		best = None
		best_score = 0
		currentPiece = workingPieces[currentPieceIndex]
		
		for rotation in range(4):
			piece = currentPiece.clone()
			for i in range(rotation):
				piece.rotate(board)
				
			while(piece.moveLeft(board)):
			    pass
			while(board.isValidPiece(piece)):
				
				pieceSet = piece.clone()
				
				while(pieceSet.moveDown(board)):
				    pass
				temp_board = board.copy()
				temp_board.addPiece(pieceSet)
				
				score = 0
				if currentPieceIndex == len(workingPieces) - 1:
					score = - self.heightWt * temp_board.get_aggregate_ht() + self.linesWt * temp_board.get_num_lines() - self.holesWt * temp_board.get_holes_count() - self.bumpinessWt * temp_board.get_bumpiness()
				else:
					best_move = self.get_best_move(temp_board, workingPieces, currentPieceIndex + 1)
					score = best_move['score']
					
				if score > best_score or best_score == 0:
					best_score = score
					best = piece.clone()
					
				piece.col = piece.col + 1
				
		return {'piece' : best, 'score' : best_score}
		
	def select_move(self, board, workingPieces):
		best_move = self.get_best_move(board, workingPieces, 0)
		return best_move['piece']
					
        
    # ai = AI_Player.AI_Player(1,1,2,1)        
    # test = Board.Board(4,5) 

    # test.cells = np.arange(20).reshape(4,5)
    # a = np.array([[11,12],[16,17]])
    # p1 = Piece.Piece(a)
    # b = np.array([[0,1],[5,6]])
    # p2 = Piece.Piece(b)

    # p = [p1, p2]
    # best = ai.select_move(test, p)