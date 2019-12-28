############### #IMPORT GAME ###############
import Reversi
############# IMPORT SYSTEM/UI ##############
import time
from io import StringIO
import sys
from ui import Gui
############## IMPORT PLAYERS ##############
#Black (first game):
import random as OPPONENT
#White (first game):
import myPlayer as ME 




############# GLOBAL VARIRABLE #############

# Write different results in the log file (player color, winner, accuracy...)
LOG_SCORE = True
#Log file path
_DIR_LOG_SCORE = "tmp/log.txt" 
#Choose mode: Multy games = True | Unique game = False
MULTY_MODE = False
#Number of games played when mutly_part function is used
NB_PARTY = 10  



############# UI INITIALIZATION #############
game_board = Gui()
game_board.show_game()



############## GAME FUNCTIONS ###############
"""
    @brief: Run NB_PARTY games 
    @param: The number of games played
    @return: The number of games won with my IA 
"""
def multy_part(nb_party):
    party = 0
    nb_win = 0
    time_min = 300
    time_max = 0
    while(party < nb_party):
        b = Reversi.Board(10)
        players = []
        if(party%2 == 0):  # alternate black and white between each game
            player1 = OPPONENT.myPlayer()
            player1.newGame(b._BLACK)
            player2 = ME.myPlayer()
            player2.newGame(b._WHITE)
            if(LOG_SCORE):
                print("\n## BLACK: ",player1.getPlayerName(),file=open(_DIR_LOG_SCORE, "a+"))
                print("## WHITE: ",player2.getPlayerName(),"\n",file=open(_DIR_LOG_SCORE, "a+"))
        else:
            player1 = ME.myPlayer()
            player1.newGame(b._BLACK)
            player2 = OPPONENT.myPlayer()
            player2.newGame(b._WHITE)
            if(LOG_SCORE):
                print("\n## BLACK: ",player1.getPlayerName(),file=open(_DIR_LOG_SCORE, "a+"))
                print("## WHITE: ",player2.getPlayerName(),"\n",file=open(_DIR_LOG_SCORE, "a+"))
            
        
       
        players.append(player1)
        players.append(player2)

        totalTime = [0,0] # total real time for each player
        nextplayer = 0
        nextplayercolor = b._BLACK
        nbmoves = 1
        outputs = ["",""]
        sysstdout= sys.stdout
        stringio = StringIO()

        while not b.is_game_over():
           
            print(b)
            nbmoves += 1
            otherplayer = (nextplayer + 1) % 2
            othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
            
            currentTime = time.time()
            sys.stdout = stringio
            move = players[nextplayer].getPlayerMove()
            sys.stdout = sysstdout
            playeroutput = "\r" + stringio.getvalue()
            stringio.truncate(0)
            print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
            outputs[nextplayer] += playeroutput
            totalTime[nextplayer] += time.time() - currentTime
            print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
            (x,y) = move 
            if not b.is_valid_move(nextplayercolor,x,y):
                print(otherplayer, nextplayer, nextplayercolor)
                print("Problem: illegal move")
                break
               
            # UI
            availMove = [m for m in players[nextplayer]._board.legal_moves()]
            (nbB, nbW) = b.get_nb_pieces()
            game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
                
            b.push([nextplayercolor, x, y])
            game_board.clear_board(b)
            (nbB, nbW) = b.get_nb_pieces()
            game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
            availMove = None
           
            players[otherplayer].playOpponentMove(x,y)

            nextplayer = otherplayer
            nextplayercolor = othercolor

        print("The game is over")
        print(b)
        (nbwhites, nbblacks) = b.get_nb_pieces()
        if(LOG_SCORE):
            print("PARTY: ",party+1,file=open(_DIR_LOG_SCORE, "a+"))
            print("Time:", totalTime,file=open(_DIR_LOG_SCORE, "a+"))
            print("Winner: ", end="",file=open(_DIR_LOG_SCORE, "a+"))

        print("PARTY: ",party)
        print("Time:", totalTime)
        print("Winner: ", end="")
        if(party%2 == 0):
            p = player2
        else:
            p = player1
        if(totalTime[p._mycolor-1] < time_min):
            time_min = totalTime[p._mycolor-1]
        if(totalTime[p._mycolor-1] > time_max):
            time_max = totalTime[p._mycolor-1]
        if nbwhites > nbblacks:
            if(party%2 == 0):
                nb_win+=1
            if(LOG_SCORE):
                print("WHITE\n\n",file=open(_DIR_LOG_SCORE, "a+"))
            print("WHITE")
        elif nbblacks > nbwhites:
            if(party%2 != 0):
                nb_win+=1
            if(LOG_SCORE):
                print("BLACK\n\n",file=open(_DIR_LOG_SCORE, "a+"))
            print("BLACK")
        else:
            if(LOG_SCORE):
                print("DEUCE\n\n",file=open(_DIR_LOG_SCORE, "a+"))
            print("DEUCE")
        
        party+=1
        print("\nWIN: ",nb_win,"/",party,"\n")
        print("\nWHITE: ",nbwhites," BLACK: ",nbblacks,file=open("logs/log.txt", "a+"))
    return (nb_win, time_max, time_min)


"""
    @brief: Run a simple game 
    @param: void
    @return: void 
"""
def unique_party():
    b = Reversi.Board(10)
    players = []
    player1 = OPPONENT.myPlayer()
    player1.newGame(b._BLACK)
    player2 = ME.myPlayer()
    player2.newGame(b._WHITE)
    if(LOG_SCORE):
        print("\n## BLACK: ",player1.getPlayerName(),file=open(_DIR_LOG_SCORE, "a+"))
        print("## WHITE: ",player2.getPlayerName(),"\n",file=open(_DIR_LOG_SCORE, "a+"))
   
    players.append(player1)
    players.append(player2)
    totalTime = [0,0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1
    outputs = ["",""]
    sysstdout= sys.stdout
    stringio = StringIO()

    while not b.is_game_over():
        print(b)
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move 
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
           
        # UI
        availMove = [m for m in players[nextplayer]._board.legal_moves()]
        (nbB, nbW) = b.get_nb_pieces()
        game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
            
        b.push([nextplayercolor, x, y])
        game_board.clear_board(b)
        (nbB, nbW) = b.get_nb_pieces()
        game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
        availMove = None
        
        players[otherplayer].playOpponentMove(x,y)
        nextplayer = otherplayer
        nextplayercolor = othercolor
        
    print("The game is over")
    print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    if(LOG_SCORE):
        print("Time:", totalTime,file=open(_DIR_LOG_SCORE, "a+"))
        print("Winner: ", end="",file=open(_DIR_LOG_SCORE, "a+"))
    print("Time:", totalTime)
    print("Winner: ", end="")
    win = 0
    if nbwhites > nbblacks:
        win += 1
        if(LOG_SCORE):
            print("WHITE\n\n",file=open(_DIR_LOG_SCORE, "a+"))
        print("WHITE")
    elif nbblacks > nbwhites:
        if(LOG_SCORE):
            print("BLACK\n\n",file=open(_DIR_LOG_SCORE, "a+"))
        print("BLACK")
    else:
        if(LOG_SCORE):
            print("DEUCE\n\n",file=open(_DIR_LOG_SCORE, "a+"))
        print("DEUCE")
    if(LOG_SCORE):
        print("\nWHITE: ",nbwhites," BLACK: ",nbblacks,file=open(_DIR_LOG_SCORE, "a+"))
   



############### CALL PARTY #################

if(MULTY_MODE):
    (win, tmax, tmin) = multy_part(NB_PARTY)
    if(LOG_SCORE):
        accuracy = 100*win/NB_PARTY
        print("\nNB Win: ",win,"/",NB_PARTY,"\nACCURACY: %0.2f" % accuracy,"%",file=open(_DIR_LOG_SCORE, "a+"))
        print("Worst time: ",tmax,"\nBest time: ",tmin,"\n\n",file=open(_DIR_LOG_SCORE, "a+"))
else:
    unique_party()
   


