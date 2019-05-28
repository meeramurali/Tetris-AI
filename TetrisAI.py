from Board import *
from Random_Piece_Generator import *
from AI_Player import *
import pygame

CellSize = 20
BoardNumRows = 20
BoardNumCols = 10

colors = {
	0 : (255, 255, 255),	# white (background color)
	1 : (255, 0, 0),		# red
	2 : (153, 204, 0),		# green
	3 : (0, 51, 204),		# blue
	4 : (255, 153, 51),		# orange
	5 : (153, 153, 255),	# purple
	6 : (255, 204, 0),		# yellow
	7 : (51, 204, 204)		# teal
}


class TetrisAI:
	def __init__(self):
		self.board = Board(BoardNumRows, BoardNumCols)
		self.piece_generator = Random_Piece_Generator()
		self.curr_piece_list = [self.piece_generator.nextPiece()]
		self.curr_piece = None
		self.ai_agent = AI_Player()
		self.score = 0


	def quit(self):
		# TODO: display exit message
		pygame.quit()


	def run(self):
		pygame.init()

		# Initialize game window w/ caption and white background
		self.window = pygame.display.set_mode((BoardNumCols * CellSize, BoardNumRows * CellSize))
		pygame.display.set_caption("TetrisAI")
		self.window.fill(colors[0])

		running = True
		while running:
			# Render board
			# self.draw(self.board.cells, 0, 0)
			# pygame.display.update()

			self.curr_piece_list.pop(0)
			self.curr_piece_list.append(self.piece_generator.nextPiece())

			# Get next best piece position
			self.curr_piece = self.ai_agent.best(self.board, self.curr_piece_list)

			# Drop piece
			reached_bottom = False
			while not reached_bottom:
				if not self.curr_piece.moveDown(self.board):
					reached_bottom = True
				else:
					self.window.fill(colors[0])
					self.draw(self.board.cells, 0, 0)
					self.draw(self.curr_piece.cells, self.curr_piece.row, self.curr_piece.col)
					# pygame.display.update()

			# Add current piece to board
			self.board.addPiece(self.curr_piece)

			# Clear lines
			self.score += self.board.clearLines()

			# Check if game over
			if self.board.isFull():
				print("Game Over!")
				running = False

			# Quit if window closed by player
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

		self.quit()


	# This function can be used to draw the board or an individual piece
	# by passing in the corresponding cells as the color matrix
	# Note: grid_row, grid_col refer to row# and col# of top left cell in matrix
	def draw(self, color_matrix, grid_row, grid_col):
		# for each colored (non-zero) cell in matrix
		for y, row in enumerate(color_matrix):
			for x, val in enumerate(row):
				if val != 0:
					# find relative position of cell on board
					pos_x = (grid_col + x) * CellSize
					pos_y = (grid_row + y) * CellSize
					# draw cell 
					pygame.draw.rect(self.window, colors[val], (pos_x, pos_y, CellSize, CellSize))
					pygame.display.update()



# class testPiece:
# 	def __init__(self, cells, row, col):
# 		self.cells = np.array(cells)
# 		self.row = row
# 		self.col = col

# test = TetrisAI()
# pcells = np.array([[0,0,0,0],[7,7,7,7],[0,0,0,0],[0,0,0,0]])
# p1 = Piece(pcells)
# p1.rotate(test.board)
# p1.rotate(test.board)
# p1.rotate(test.board)
# p1.rotate(test.board)
# test.board.addPiece(p1)

# p2 = Piece().select_piece(2)
# p2.rotate(test.board)
# test.board.addPiece(p2)
# test.run()

test1 = TetrisAI()
# print(test1.ai_agent.best(test1.board, test1.curr_piece_list))
test1.run()
