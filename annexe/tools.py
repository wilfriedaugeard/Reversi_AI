################# IMPORTS ##################
from random import randint
import time

############# GLOBAL VARIRABLE #############
# Time to play a move
TIME_MAX = 6 
# Maximum Time to play a game
TIME_PARTY = 300 

############# MOVE FUNCTIONS ###############
"""
    @brief: Check if the move is on a corner
    @param: The move
    @return: A boolean 
"""
def isCorner(move):
    (c, i, j) = move
    return ((i == 0 and j == 0) or
            (i == 0 and j == 9) or
            (i == 9 and j == 0) or
            (i == 9 and j == 9))


"""
    @brief: Check if the move is a priority move that's mean a move which kill the opponent or take a corner
    @param: The board and the move
    @return: A boolean 
"""
def killer_move(board, move):
    return (board.is_game_over() or isCorner(move))


"""
    @brief: Check if the given move is a forbidden move that's mean it's a neighbour of a corner and the corner is empty or taken by the opponent 
    @param: The player, the board and the move
    @return: A boolean
"""
def isCornerNeighbour(self, board,move):
    (x,c,l) = move
    return(((c==1 and l==1 ) and board._board[0][0] != self._mycolor) or
        ((c==1 and l==8 ) and board._board[0][9] != self._mycolor) or
        ((c==8 and l==1 ) and board._board[9][0] != self._mycolor) or
        ((c==8 and l==8 ) and board._board[9][9] != self._mycolor) or
        ((l==0 and c==1 ) and board._board[0][0] != self._mycolor) or 
        ((l==1 and c==0 ) and board._board[0][0] != self._mycolor) or
        ((l==0 and c==8 ) and board._board[9][0] != self._mycolor) or
        ((l==8 and c==0 ) and board._board[0][9] != self._mycolor) or 
        ((l==9 and c==1 ) and board._board[0][9] != self._mycolor) or
        ((l==1 and c==9 ) and board._board[9][0] != self._mycolor) or
        ((l==8 and c==9 ) and board._board[9][9] != self._mycolor) or 
        ((l==9 and c==8 ) and board._board[9][9] != self._mycolor))


"""
    @brief: Get a random move
    @param: The board
    @return: The random move
"""
def getRandomMove(board):
    moves = [m for m in board.legal_moves()]
    return moves[randint(0,len(moves)-1)]


############# PLAYER FUNCTIONS ###############
"""
    @brief: Get the number of turns remaining for the player
    @param: The player and the board
    @return: The number of turns
"""
def getRestNbTurn(self, board):
    board_size = board._boardsize*board._boardsize
    laps = (board_size-4)/2 # take off 4 -> the already played coins at the beginning of the game
    return (laps-self._tours)


"""
    @brief: Get the number of player's coins
    @param: The player and the board
    @return: The number of player's coins 
"""
def getMyNbCoins(self, board):
    if(self._mycolor == board._BLACK):
        return board._nbBLACK
    else:
        return board._nbWHITE


"""
    @brief: Check if a player win
    @param: The player and the board
    @return: A boolean
"""
def myIA_win(self, board):
    if(self._mycolor == board._BLACK):
        return board._nbBLACK > board._nbWHITE
    else:
        return board._nbWHITE > board._nbBLACK


############# OTHER FUNCTIONS ################
"""
    @brief: Check if the player has the time to play
    @param: The player, the time at the beginning of the turn and the board
    @return: A boolean
"""
def timeOver(self, currentTime, board):
    t = (time.time() - currentTime)
    return self._totalTime+t > TIME_PARTY- (getRestNbTurn(self, board)*TIME_MAX) # Check if the total time don't exceed the limited time for this move