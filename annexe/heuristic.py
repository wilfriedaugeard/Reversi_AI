################## IMPORTS #################
import math



############# GLOBAL VARIRABLE #############
#Weight of a priority move
PRIORITY_COEFF = 10
#Weight of a bad strategy move (the line before edges and corners)
BAD_MOVE = -5



################ HEURISTICS ################
"""
    @brief: Compute heuristic about positions with a board given
    @param: The player and the board
    @return: The heuritics computed 
"""
def edge_eval_v2(self,board):
        corners = [[1,1],[1,10], [10,1], [10,10]]
        other_player = self._opponent
        score = 0
        
        for i in range(10):
            for j in range(10):
                delta = 1
                if(
                    (i == 0 and j == 0) or
                    (i == 0 and j == 9) or
                    (i == 9 and j == 0) or
                    (i == 9 and j == 9)):
                    delta += PRIORITY_COEFF
                    
                if i == 0 or i == 9:
                    delta += 5
                if j == 0 or j == 9:
                    delta += 5

                if i == 1 or i == 8:
                    delta += BAD_MOVE
                if j == 1 or j == 8:
                    delta += BAD_MOVE

                for corner in corners:
                    distX = abs(corner[0] - i)
                    distY = abs(corner[1] - j)
                    dist  = math.sqrt(distX*distX + distY*distY)
                    if dist < 4:
                        delta += 3
                
                if board._board[i][j] == self._mycolor:
                    score += delta
                elif board._board[i][j] == other_player:
                    score -= delta

        for l in range(board._boardsize):
            for c in range(l):
                delta = 1
                if(
                    (l == 0 and c == 0) or
                    (l == 0 and c == 9) or
                    (l == 9 and c == 0) or
                    (l == 9 and c == 9)):
                    delta += PRIORITY_COEFF
                if l == 0 or l == 9:
                    delta += 5
                if c == 0 or c == 9:
                    delta += 5

                if l == 1 or l == 8:
                    delta += BAD_MOVE
                if c == 1 or c == 8:
                    delta += BAD_MOVE

                for corner in corners:
                    distX = abs(corner[0] - l)
                    distY = abs(corner[1] - c)
                    dist  = math.sqrt(distX*distX + distY*distY)
                    if dist < 4:
                        delta += 3

                if c == self._mycolor:
                    score += delta
                elif c == other_player:
                    score -= delta  
        return score