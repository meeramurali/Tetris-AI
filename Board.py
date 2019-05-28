import numpy as np
from Piece import *

class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.cells = np.zeros((rows, cols), dtype=int)


	def copy(self):
		copy = Board(self.rows, self.cols)
		copy.cells = np.ndarray.copy(self.cells)
		return copy


	def isLine(self, row_index):
		for col_index in range(self.cols):
			if self.cells[row_index][col_index] == 0:
				return False
		return True


	def isEmptyRow(self, row_index):
		for col_index in range(self.cols):
			if self.cells[row_index][col_index] != 0:
				return False
		return True


	def clearLines(self):
		num_cleared = 0

		# For each row...
		for row in range((self.rows - 1), 0, -1):
			# if its a line, clear it (set to 0s)
			if self.isLine(row):
				for col in range(self.cols):
					self.cells[row][col] = 0
				num_cleared += 1
			# otherwise shift row down by number of lines cleared so far
			elif num_cleared > 0:
				for col in range(self.cols):
					self.cells[row + num_cleared][col] = self.cells[row][col]
					self.cells[row][col] = 0

		return num_cleared


	def isFull(self):
		return not (self.isEmptyRow(0) and self.isEmptyRow(1))


	def get_height(self):
		# Count number of empty rows
		num_empty_rows = 0
		row = 0
		while row < self.rows and self.isEmptyRow(row):
			num_empty_rows += 1
			row += 1

		# Height = total no. of rows - no. of empty rows
		return self.rows - num_empty_rows


	def get_num_lines(self):
		num_lines = 0
		for row in range(self.rows):
			if (self.isLine(row)):
				num_lines += 1
		return num_lines


	def get_column_ht(self, col):
		num_empty_rows = 0
		row = 0
		while row < self.rows and self.cells[row][col] == 0:
			num_empty_rows += 1
			row += 1

		# Height = total no. of rows - no. of empty rows
		return self.rows - num_empty_rows


	def get_aggregate_ht(self):
		agg_ht = 0
		for col in range(self.cols):
			agg_ht += self.get_column_ht(col)
		return agg_ht


	def get_holes_count(self):
		num_holes = 0
		for col in range(self.cols):
			isblock = False
			for row in range(self.rows):
				if self.cells[row][col] != 0:
					isblock = True
				elif self.cells[row][col] == 0 and isblock:
					num_holes += 1
		return num_holes


	def get_bumpiness(self):
		bumpiness = 0
		# bumpiness = sum of differences in heights of adjacent columns
		for col in range(self.cols - 1):
			bumpiness += abs(self.get_column_ht(col) - self.get_column_ht(col + 1))
		return bumpiness


	def get_blockage_count(self):
		num_blockages = 0
		for col in range(self.cols):
			ishole = False
			for row in range(self.rows - 1, 0, -1):
				if self.cells[row][col] == 0:
					ishole = True
				elif self.cells[row][col] != 0 and ishole:
					num_blockages += 1
		return num_blockages


	def isValidPiece(self, piece):
		for row in range(len(piece.cells)):
			for col in range(len(piece.cells[row])):
				pos_row = piece.row + row
				pos_col = piece.col + col

				# if out of bounds of grid, piece is invalid
				if (pos_row < 0 or pos_row >= self.rows) \
					or (pos_col < 0 or pos_col >= self.cols):
					return False

				# if cell is already filled in board, piece is invalid
				elif self.cells[pos_row][pos_col] != 0:
					return False

		return True


	def addPiece(self, piece):
		for row in range(len(piece.cells)):
			for col in range(len(piece.cells[row])):
				# Find relative cell position in board
				pos_row = piece.row + row
				pos_col = piece.col + col
				# Fill cell
				if piece.cells[row][col] != 0 and pos_row >= 0:
					self.cells[pos_row][pos_col] = piece.cells[row][col]



# test = Board(10, 10)
# print(test.cells)
# print(test.copy().cells)
# print(test.isLine(0))
# print(test.isEmptyRow(2))
# for col in range(test.cols):
# 	test.cells[len(test.cells) - 1][col] = 1
# 	test.cells[len(test.cells) - 3][col] = 1
# 	if col != 0 and col != 1:
# 		test.cells[len(test.cells) - 2][col] = 1
# test.cells[1][0] = 0
# print(test.cells)
# # test.clearLines()
# print(test.cells)
# # test.cells = np.ones((10, 10), dtype= int)
# print("is_Full", test.isFull())
# # test.clearLines()
# print(test.cells)
# print(test.get_height())
# print(test.get_num_lines())
# print(test.get_column_ht(0))
# print(test.get_aggregate_ht())
# print(test.get_holes_count())
# print(test.get_bumpiness())
# print(test.get_blockage_count())

# # class testPiece:
# # 	def __init__(self, row, col):
# # 		self.cells = np.ones((2,2))
# # 		self.row = row
# # 		self.col = col

# pcells = np.ones((2,2))
# test_piece = Piece(pcells)
# if test.isValidPiece(test_piece):
# 	test.addPiece(test_piece)
# 	print(test.cells)
# else:
# 	print("invalid piece")









