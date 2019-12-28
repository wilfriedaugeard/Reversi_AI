################# IMPORTS ##################
import time
from annexe.tools import *



############# GLOBAL VARIRABLE #############
#Infini
INFINI = 1000000
#Write different results in a file (move, best move, heuritics, time...)
LOG_HEURISTIC = True
#The file path
_DIR_LOG_HEURISTIC = "tmp/heuristic.txt"



################ ALPHA BETA ################
"""
    @brief: Alphabeta when it's the player turn 
    @param: The player, the board, the depth, alpha and beta, the heuristic function,
            the time corresponding to the begin of the turn
    @return: The value compute by the heuristic function
"""
def alphabeta_value_ami(self, board, depth, alpha, beta, eval, currentTime):
    if depth == 0:
        return eval(self,board) #Heuristic
    
    for move in board.legal_moves():
        board.push(move)  

        if beta != INFINI:
            next_alpha = -1 * beta
        else:
            next_alpha = - 1 * INFINI
        if alpha != -1 * INFINI:
            next_beta = -1 * alpha
        else:
            next_beta = INFINI

        if(timeOver(self, currentTime, board)):  #Check if the player has exceeded the time
            print("TIME OVER: ",time.time()-currentTime," | ", self._tours,file=open("logs/log.txt", "a+"))
            board.pop()
            return alpha

        val = -1 * alphabeta_value_ennemi(self, board, depth-1, next_alpha, next_beta, eval,currentTime)  #Recursion with the opponent turn

        board.pop()
        if alpha == -1 * INFINI or val > alpha:
            alpha = val

        if (alpha !=  -1 * INFINI) and (beta != INFINI) and alpha >= beta:
            return beta  

    return alpha


"""
    @brief: Alphabeta when it's the opponent turn 
    @param: The player, the board, the depth, alpha and beta, the heuristic function,
            the time corresponding to the begin of the turn
    @return: The value compute by the heuristic function
"""
def alphabeta_value_ennemi(self, board, depth, alpha, beta, eval,currentTime):
    if depth == 0:
        return eval(self,board)
    
    for move in board.legal_moves():
        (c,x,y) = move
        board.push([self._opponent, x, y])

        if beta != INFINI:
            next_alpha = -1 * beta
        else:
            next_alpha = - 1 * INFINI
        if alpha != -1 * INFINI:
            next_beta = -1 * alpha
        else:
            next_beta = INFINI
        
        if(timeOver(self, currentTime, board)):  #Check if the player has exceeded the time
            print("TIME OVER: ",time.time()-currentTime," | ", self._tours,file=open("logs/log.txt", "a+"))
            board.pop()
            return alpha

        val = -1 * alphabeta_value_ami(self, board, depth-1, next_alpha, next_beta, eval,currentTime)  #Recursion with the player turn

        board.pop()
        if alpha == -1 * INFINI or val > alpha:
            alpha = val

        if (alpha !=  -1 * INFINI) and (beta != INFINI) and alpha >= beta:
            return beta

    return alpha




############# DFS STATISTICS ###############
"""
    @brief: Execute a Depth-First Search and give the probabitlity to win when it's player turn. 
    @param: The player, the board, the depth and the time corresponding to the begin of the turn
    @return: A probability (the sum of won moves divided by the total of moves) 
"""
def moyenne_search_ami(self, board, depth,currentTime):
    if depth == 0:
        if(board.is_game_over() and myIA_win(self, board)):
            return 1
        else:
            return 0
           
    somme = 0
    for move in board.legal_moves():
        board.push(move)

        if(timeOver(self, currentTime, board)):  #Check if the player has exceeded the time
            board.pop()
            return 0 

        somme += moyenne_search_ennemi(self, board, depth-1,currentTime)  #Recursion with the opponent turn
        board.pop()

    return somme/len(board.legal_moves())


"""
    @brief: Execute a Depth-First Search and give the probabitlity to win when it's opponent turn. 
    @param: The player, the board, the depth and the time corresponding to the begin of the turn
    @return: A probability (the sum of won moves divided by the total of moves) 
"""
def moyenne_search_ennemi(self, board, depth,currentTime):
    if depth == 0:
        if(board.is_game_over() and myIA_win(self, board)):
            return 1
        else:
            return 0

    somme = 0
    for move in board.legal_moves():
        (c,x,y) = move
        board.push([self._opponent, x, y])

        if(timeOver(self, currentTime, board)):  #Check if the player has exceeded the time
            board.pop()
            return 0

        somme += moyenne_search_ami(self, board, depth-1,currentTime)  #Recursion with the player turn
        board.pop()

    return somme/len(board.legal_moves()) 




############## BEST MOVE ##################
"""
    @brief: Execute alphaBeta or dfs statistics during the game
    @param: The player, the board, the depth and the heuritic function
    @return: The best move computed
"""
def bestMove(self, board, depth, eval):
    self._tours += 1
    currentTime = time.time()

    best_val, best_move = INFINI, getRandomMove(board)
    best_current_nb_coins = 2
    val = INFINI
         
    nb_rest = getRestNbTurn(self, board)  #Get the number of remaining turns 

    #----- END GAME ----#
    if(nb_rest < 5):
        depth = nb_rest
        best_val = -1*INFINI

        for move in board.legal_moves():
            board.push(move)

            if(board.is_game_over() and myIA_win(self, board)):  #Check if the move kill the opponent
                board.pop()
                self._totalTime += (time.time() - currentTime)
                return move

            if(timeOver(self, currentTime, board)):  #Check if the time is over for this move
                board.pop()
                self._totalTime += (time.time() - currentTime)
                return move

            val = moyenne_search_ennemi(self, board, depth, currentTime)  #Recursion with the dfs statistics
        
            if best_val == INFINI or val > best_val:  #Get the best value
                (best_val, best_move) = (val, move) 
            board.pop()

            if(LOG_HEURISTIC):
                print("MOVE; ",move,"\nVAL HEURISTIC: ",val,"\n", file=open(_DIR_LOG_HEURISTIC, "a+"))
        if(LOG_HEURISTIC):
            print("\nBEST HEURISTIC: ",best_val,"\n BEST MOVE; ",best_move, file=open(_DIR_LOG_HEURISTIC, "a+"))


    #----- BEGIN/MIDDLE GAME ----#
    else:
        for move in board.legal_moves():
            board.push(move)

            if(killer_move(board, move)):  #Priority move
                board.pop()
                self._totalTime += (time.time() - currentTime)
                return move


            if best_val != INFINI:
                next_beta = -1 * best_val
            else:
                next_beta = INFINI


            if(not isCornerNeighbour(self,board,move)):  #Check it's not a forbidden move
                if(timeOver(self, currentTime, board)):  #Check if the time is over for this move
                    board.pop()
                    self._totalTime += (time.time() - currentTime)
                    return move

                val = -1 * alphabeta_value_ennemi(self, board, depth, -1 * INFINI, next_beta, eval, currentTime)  #Recursion with alphabeta

                if best_val == INFINI or val > best_val:  #Get the best heuritic
                    best_current_nb_coins = getMyNbCoins(self, board)
                    (best_val, best_move) = (val, move) 
                else:
                    if(best_val == val):
                        if(getMyNbCoins(self, board) > best_current_nb_coins):  #With same heuritics between val and best_val: take the move with the most coins
                            best_current_nb_coins = getMyNbCoins(self,board)
                            (best_val, best_move) = (val, move) 

            board.pop()
            if(LOG_HEURISTIC):
                print("MOVE; ",move,"\nVAL HEURISTIC: ",val,"\n", file=open(_DIR_LOG_HEURISTIC, "a+"))
        if(LOG_HEURISTIC):
            print("\nBEST HEURISTIC: ",best_val,"\n BEST MOVE; ",best_move, file=open(_DIR_LOG_HEURISTIC, "a+"))


    self._totalTime += (time.time() - currentTime)  #Add the time for this move 
    print("TIME: ",self._totalTime," | ", self._tours, file=open(_DIR_LOG_HEURISTIC, "a+"))
    return best_move

