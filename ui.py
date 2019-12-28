################ IMPORT SYS ###############
import os
import sys

############### IMPORT PYGAME ##############
import pygame
from pygame.locals import *

################ IMPORT GAME ###############
import Reversi


############## GLOBAL VARIABLE #############
BLACK=Reversi.Board._BLACK
WHITE=Reversi.Board._WHITE
__WIDTH__  = 1080
__HEIGHT__ = 720




class Gui:
    def __init__(self):
        """ Initializes graphics. """

        pygame.init()
        
        driver = pygame.display.get_driver()
        print("Using: ", driver, "driver")

        # colors
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (255, 255, 255)
        self.WHITE = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (128, 128, 0)

        # display
        self.SCREEN_SIZE = (__WIDTH__, __HEIGHT__)
        self.BOARD_POS = (100, 20) 
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 500
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        self.BLACK_LAB_POS = (__WIDTH__ - __WIDTH__/4, __HEIGHT__ / 4 +  __HEIGHT__ / 4 )
        self.WHITE_LAB_POS = (__WIDTH__ - __WIDTH__/4, __HEIGHT__ / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Serif", 58)

        # image files
        APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
        RESOURCE_FOLDER = os.path.join(APP_FOLDER, "resources")
        self.board_img = pygame.image.load(os.path.join(
            RESOURCE_FOLDER, "board.png")).convert()
        self.black_img = pygame.image.load(os.path.join(
            RESOURCE_FOLDER, "black.bmp")).convert()
        self.white_img = pygame.image.load(os.path.join(
            RESOURCE_FOLDER, "white.bmp")).convert()
        self.avail_img = pygame.image.load(os.path.join(RESOURCE_FOLDER,
                                                      "avail.bmp")).convert()
        self.clear_img = pygame.image.load(os.path.join(RESOURCE_FOLDER,
                                                        "empty.bmp")).convert()


    """
        @brief: Display the game
        @param: void
        @return: void
    """
    def show_game(self):

        # draws initial screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND)
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS,
                         self.board_img.get_rect())
        self.put_stone((4, 4), WHITE)
        self.put_stone((5, 5), WHITE)
        self.put_stone((4, 5), BLACK)
        self.put_stone((5, 4), BLACK)
        pygame.display.flip()


    """
        @brief: Draw coin with given position and color 
        @param: The position and the color
        return: void
    """
    def put_stone(self, pos, color):
        if pos == None:
            return

        pos = (pos[1], pos[0])  #Flip orientation (because xy screen orientation)

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        else:
            img = self.avail_img

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()


    """
        @brief: Clean the board
        @param: The board
        @return: void
    """
    def clear_board(self, board):
        for x in range(0,board._boardsize,1):
            for y in range(0,board._boardsize,1):
                self.clear_square((x,y))


    """
        @brief: Put in the given position a background image, to simulate that the
                piece was removed.
        @param: The position
        @return: void
    """
    def clear_square(self, pos):
        
        pos = (pos[1], pos[0])   #flip orientation

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
        pygame.display.flip()
        

    """
        @brief: Update the screen
        @param: The board, the number of black and white coins, availMove and the current player color
        @return: void
    """
    def update(self, board, blacks, whites, availMove, current_player_color):

        if(availMove is not None):
            for move in availMove:
                (_,x,y) = move
                self.put_stone((x,y), None)
        
        for x in range(0,board._boardsize,1):
            for y in range(0,board._boardsize,1):
                if board._board[y][x] != Reversi.Board._EMPTY:
                    self.put_stone((y, x), board._board[y][x])

        blacks_str = '%02d ' % int(whites)
        whites_str = '%02d ' % int(blacks)
        self.showScore(blacks_str, whites_str, current_player_color)
        pygame.display.flip()



    """
        @brief: Display the score
        @param: The string number of black and white and the current player color
        @return: void
    """
    def showScore(self, blackStr, whiteStr, current_player_color):
        black_background = self.YELLOW if current_player_color == WHITE else self.BACKGROUND
        white_background = self.YELLOW if current_player_color == BLACK else self.BACKGROUND
        text = self.scoreFont.render(blackStr, True, self.BLACK,
                                     black_background)
        text_1 = self.scoreFont.render("Black", True, self.BLACK,
                                     black_background)
        text_2 = self.scoreFont.render("White", True, self.WHITE,
                                     white_background)
        text2 = self.scoreFont.render(whiteStr, True, self.WHITE,
                                      white_background)
        self.screen.blit(text_1,
                         (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] - 40))
        self.screen.blit(text,
                         (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] + 40))
        self.screen.blit(text_2,
                         (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] - 40))
        self.screen.blit(text2,
                         (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))

    





