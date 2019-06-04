from Board import *
from Random_Piece_Generator import *
from AI_Player import *
import pygame

CellSize = 20
BoardNumRows = 20
BoardNumCols = 10
SideBarCols = 5

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
	def __init__(self, ai_params=[-0.5, 1, -0.5, -1]):
		self.board = Board(BoardNumRows, BoardNumCols)
		self.piece_generator = Random_Piece_Generator()
		self.curr_piece_list = [self.piece_generator.nextPiece()]
		self.curr_piece = None
		self.score = 0
		self.board_width = BoardNumCols * CellSize
		self.board_ht = BoardNumRows * CellSize
		self.window_width = self.board_width + (SideBarCols * CellSize)
		self.window_ht = self.board_ht
		self.heightWt = ai_params[0]
		self.linesWt = ai_params[1]
		self.holesWt = ai_params[2]
		self.bumpinessWt = ai_params[3]
		self.ai_agent = AI_Player(ai_params)


	def center_msg(self, msg):
		font =  pygame.font.Font('/System/Library/Fonts/Helvetica.ttc', 24)
		for i, line in enumerate(msg.splitlines()):
			msg_image =  font.render(line, False, (0,0,0), (255,255,255))
		
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
		
			self.window.blit(msg_image, (
			  self.window_width // 2 - msgim_center_x,
			  self.window_ht // 2 - msgim_center_y + i * 22))


	def draw_score(self):
		score_text = """Score:\n%d""" % self.score
		font =  pygame.font.Font('/System/Library/Fonts/Helvetica.ttc', 20)
	
		for i, line in enumerate(score_text.splitlines()):
			image =  font.render(line, False, (0,0,0), (255,255,255))
			center_x, center_y = image.get_size()
			center_x //= 2
			center_y //= 2
		
			self.window.blit(image, (
			  (self.board_width) + ((SideBarCols * CellSize) // 2 - center_x),
			  ((self.window_ht) // 2 - center_y + i * 30)))


	def draw_ai_parameters(self):
		param_text = """heightWt: %f\nlinesWt: %f\nholesWt: %f\nbumpWt: %f""" \
			% (self.heightWt, self.linesWt, self.holesWt, self.bumpinessWt)
		font =  pygame.font.Font('/System/Library/Fonts/Helvetica.ttc', 11)
		for i, line in enumerate(param_text.splitlines()):
			image =  font.render(line, False, (0,0,0), (255,255,255))
		
			center_x, center_y = image.get_size()
			center_x //= 2
			center_y //= 2
		
			self.window.blit(image, (
			  (self.board_width) + ((SideBarCols * CellSize) // 2 - center_x),
			  ((2 * self.window_ht) // 3 - center_y + i * 20) + 3 * CellSize)) 


	def draw_next_piece(self):
		text = """Next:"""
		font =  pygame.font.Font('/System/Library/Fonts/Helvetica.ttc', 20)
		image =  font.render(text, False, (0,0,0), (255,255,255))

		center_x, center_y = image.get_size()
		center_x //= 2
		center_y //= 2
	
		self.window.blit(image, (
		  (self.board_width) + ((SideBarCols * CellSize) // 2 - center_x),
		  (1 * CellSize)))

		next_piece = self.curr_piece_list[0]
		self.draw(next_piece.cells, 3, BoardNumCols + 1)


	def run(self):
		pygame.init()

		# Initialize game window w/ caption and white background
		self.window = pygame.display.set_mode((self.window_width, self.window_ht))
		pygame.display.set_caption("TetrisAI")
		self.window.fill(colors[0])
		

		running = True
		while running:
			# Check if game over
			if self.board.isFull():
				self.center_msg("""Game Over!\nYour score: %d""" % self.score)
				print("Score:", self.score)
				print("Game Over!")
				running = False

			else:
				# Render board
				# self.draw(self.board.cells, 0, 0)
				# pygame.display.update()

				self.curr_piece_list.pop(0)
				self.curr_piece_list.append(self.piece_generator.nextPiece())

				# Get next best piece position
				self.curr_piece = self.ai_agent.select_move(self.board, self.curr_piece_list)

				# Drop piece
				reached_bottom = False
				while not reached_bottom and self.curr_piece is not None:
					if not self.curr_piece.moveDown(self.board):
						reached_bottom = True
					else:
						self.window.fill(colors[0])
						pygame.draw.line(self.window, (0, 0, 0), (self.board_width, 0), (self.board_width, self.window_ht))
						self.draw(self.board.cells, 0, 0)
						self.draw(self.curr_piece.cells, self.curr_piece.row, self.curr_piece.col)
						self.draw_next_piece()
						self.draw_score()
						self.draw_ai_parameters()
						pygame.display.update()

				# Add current piece to board
				if self.curr_piece is not None:
					self.board.addPiece(self.curr_piece)

				# Clear lines
				self.score += self.board.clearLines()

			# Quit if window closed by player
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

		pygame.quit()


	def run_trainMode(self, max_moves):
		total_moves = 0
		while not self.board.isFull() and total_moves < max_moves:
			self.curr_piece_list.pop(0)
			self.curr_piece_list.append(self.piece_generator.nextPiece())

			# Get next best piece position
			self.curr_piece = self.ai_agent.select_move(self.board, self.curr_piece_list)

			# Drop piece
			reached_bottom = False
			while not reached_bottom and self.curr_piece is not None:
				if not self.curr_piece.moveDown(self.board):
					reached_bottom = True

			# Add current piece to board
			if self.curr_piece is not None:
				self.board.addPiece(self.curr_piece)

			# Clear lines
			self.score += self.board.clearLines()

			total_moves += 1


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
					# pygame.display.update()



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

# test1 = TetrisAI()
# test1.run()
# print(test1.score)
# # print(test1.ai_agent.best(test1.board, test1.curr_piece_list))

