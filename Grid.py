import numpy as np

class Grid:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.cells = np.zeros((rows, cols), dtype=int)


	def copy(self):
		copy = Grid(self.rows, self.cols)
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


	def exceeded(self):
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



# test = Grid(4, 4)
# print(test.cells)
# print(test.clone().cells)
# print(test.isLine(0))
# print(test.isEmptyRow(2))
# for col in range(test.cols):
# 	test.cells[1][col] = 1
# 	test.cells[3][col] = 1
# 	if col != 0:
# 		test.cells[2][col] = 1
# print(test.cells)
# test.clearLines()
# print(test.cells)
# test.cells = np.ones((4, 4), dtype= int)
# print(test.exceeded())
# print(test.cells)
# print(test.get_height())
# print(test.get_num_lines())











