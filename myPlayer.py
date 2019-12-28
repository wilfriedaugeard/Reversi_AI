################ IMPORT GAME ###############
import Reversi

########### IMPORT PLAYER ANNEXE ###########
from playerInterface import *
from annexe.alpha_beta import *
from annexe.heuristic import *


class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

        # Total time taken by my IA during the game
        self._totalTime = 0
        # Number of turns
        self._tours = 0

    def getPlayerName(self):
        return "Will IA"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        board = self._board
        move = bestMove(self, board, 3, edge_eval_v2) #Get the best move

        self._board.push(move)
        (c,x,y) = move 
        assert(c==self._mycolor)

        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


    