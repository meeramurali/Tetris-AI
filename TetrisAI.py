from Board import *
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

	def quit(self):
		# TODO: display exit message
		pygame.quit()

	def run(self):
		pygame.init()

		# Initialize game window w/ caption and white background
		self.window = pygame.display.set_mode((BoardNumCols * CellSize, BoardNumRows * CellSize))
		pygame.display.set_caption("TetrisAI")
		self.window.fill(colors[0])
		pygame.display.update()

		running = True
		while running:
			# Render board
			self.draw(self.board.cells, 0, 0)
			pygame.display.update()

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


# import numpy as np
# class testPiece:
# 	def __init__(self, cells, row, col):
# 		self.cells = np.array(cells)
# 		self.row = row
# 		self.col = col
# p1 = testPiece([[0, 2, 0], [2, 2, 2], [0, 0, 0]], BoardNumRows - 2, 0)
# p2 = testPiece([[0, 1, 0], [1, 1, 1], [0, 0, 0]], BoardNumRows - 2, 3)

# test = TetrisAI()
# test.board.addPiece(p1)
# test.board.addPiece(p2)
# test.run()

