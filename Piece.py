import numpy as np
import math

class Piece:
    
    def __init__(self, cells=np.empty(0)):
        self.cells = cells
        self.dimension = cells.shape[0]
        self.row = 0 
        self.col = 0

    
    def select_piece(self, index):
        
        if index == 0:
            piece = Piece(np.array([[3,3],[3,3]]))
        
        elif index == 1:
            piece = Piece(np.array([[1,0,0],[1,1,1],[0,0,0]]))
            
        elif index == 2:
            piece = Piece(np.array([[0,0,2],[2,2,2],[0,0,0]]))
            
        elif index == 3:
             piece = Piece(np.array([[4,4,0],[0,4,4],[0,0,0]]))
                
        elif index == 4:
             piece = Piece(np.array([[0,5,5],[5,5,0],[0,0,0]]))
                
        elif index == 5:
             piece = Piece(np.array([[0,6,0],[6,6,6],[0,0,0]]))
                
        elif index == 6:
             piece = Piece(np.array([[0,0,0,0],[7,7,7,7],[0,0,0,0],[0,0,0,0]]))
        
        piece.row = 0
        piece.col = math.floor((10 - piece.dimension) / 2)
        return piece
    
    
    def clone(self):
        copy_cells = np.empty_like (self.cells)
        copy_cells[:] = self.cells
        piece = Piece(copy_cells)
        piece.row = self.row
        piece.col = self.col
        return piece
        
    
    def checkLeftMove(self, board):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                pos_row = self.row + row
                pos_col = self.col - 1
                if self.cells[row][col] != 0 :
                    if not (pos_col >= 0 and board.cells[pos_row][pos_col] == 0):
                        return False
                
        return True       
        
    
    
    def checkRightMove(self, board):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                pos_row = self.row + row
                pos_col = self.col + 1
                if self.cells[row][col] != 0 :
                    if not (pos_col >= 0 and board.cells[pos_row][pos_col] == 0):
                        return False
                
        return True   
       
    
    
    def checkDownMove(self, board):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                pos_row = self.row + row + 1
                pos_col = self.col + col
                if self.cells[row][col] != 0  and pos_row >= 0 :
                    if not (pos_row < board.rows and board.cells[pos_row][pos_col] == 0):
                        return False
                
        return True   
       
   
    def moveLeft(self, board):
        if not self.checkLeftMove(board):
            return False
    
        self.col = self.col - 1
        return True
        
    
    def moveRight(self, board):
        if not self.checkRightMove(board):
            return False
    
        self.col = self.col + 1
        return True
        
    
    def moveDown(self, board):
        if not self.checkDownMove(board):
            return False
    
        self.row = self.row + 1
        return True
    
    def rotateCells(self):
        copy_cell = np.empty_like(self.cells)
        
        if self.dimension == 2:
            copy_cell[0][0] = self.cells[1][0]
            copy_cell[0][1] = self.cells[0][0]
            copy_cell[1][0] = self.cells[1][1]
            copy_cell[1][1] = self.cells[0][1]
            
        elif self.dimension == 3:
            copy_cell[0][0] = self.cells[2][0]
            copy_cell[0][1] = self.cells[1][0]
            copy_cell[0][2] = self.cells[0][0]
            copy_cell[1][0] = self.cells[2][1]
            copy_cell[1][1] = self.cells[1][1]
            copy_cell[1][2] = self.cells[0][1]
            copy_cell[2][0] = self.cells[2][2]
            copy_cell[2][1] = self.cells[1][2]
            copy_cell[2][2] = self.cells[0][2]
            
        elif self.dimension == 4:
            copy_cell[0][0] = self.cells[3][0]
            copy_cell[0][1] = self.cells[2][0]
            copy_cell[0][2] = self.cells[1][0]
            copy_cell[0][3] = self.cells[0][0]
            copy_cell[1][3] = self.cells[0][1]
            copy_cell[2][3] = self.cells[0][2]
            copy_cell[3][3] = self.cells[0][3]
            copy_cell[3][2] = self.cells[1][3]
            copy_cell[3][1] = self.cells[2][3]
            copy_cell[3][0] = self.cells[3][3]
            copy_cell[2][0] = self.cells[3][2]
            copy_cell[1][0] = self.cells[3][1]

            copy_cell[1][1] = self.cells[2][1]
            copy_cell[1][2] = self.cells[1][1]
            copy_cell[2][2] = self.cells[1][2]
            copy_cell[2][1] = self.cells[2][2]
            
        self.cells = copy_cell
        
    def calculateOffset(self, board):
        temp_piece = self.clone()
        
        temp_piece.rotateCells()
        
        if board.isValidPiece(temp_piece):
            offset = {'rowOffset': temp_piece.row - self.row, 'columnOffset': temp_piece.col - self.col}
            return offset
        
        initialRow = temp_piece.row
        initialCol = temp_piece.col
        
        
        for i in range(self.dimension - 1):
            temp_piece.col = initialCol + i
            if board.isValidPiece(temp_piece):
                offset = {'rowOffset' : temp_piece.row - self.row, 'columnOffset' : temp_piece.col - self.col} 
                return offset
            
            for j in range(self.dimension - 1):
                temp_piece.row = initialRow - j
                if board.isValidPiece(temp_piece):
                    offset = {'rowOffset' : temp_piece.row - self.row, 'columnOffset' : temp_piece.col - self.col}
                    return offset
                
            temp_piece.row = initialRow
            
        temp_piece.col = initialCol
        
        
        for i in range(self.dimension - 1):
            temp_piece.col = initialCol - i
            if board.isValidPiece(temp_piece):
                offset = {'rowOffset' : temp_piece.row - self.row, 'columnOffset' : temp_piece.col - self.col}
                return offset
            
            for j in range(self.dimension - 1):
                temp_piece.row = initialRow - j
                if board.isValidPiece(temp_piece):
                    offset = {'rowOffset' : temp_piece.row - self.row, 'columnOffset' : temp_piece.col - self.col}
                    return offset
            temp_piece.row = initialRow
            
        temp_piece.col = initialCol
        
        
        return None
    
    def rotate(self, board):
        offset = self.calculateOffset(board)
        
        if offset != None:
            self.rotateCells()
            self.row = self.row + offset['rowOffset']
            self.col = self.col + offset['columnOffset']
                    
                
    
        