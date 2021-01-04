"""
File: royal_game_of_ur.py
Author: Amarjot Gill
Date: 10/31/2020
Lab Section: 44
Email:  agill3@umbc.edu
Description:  This program will uses Classes in order
to play a 2 player game of the royal_game_of_ur
using many helper functions within the class the main game
is played within the play_game function
"""

from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece
# these are the magical values in my project
WHITE = "White"
BLACK = "Black"
PLAYER1 = "player1"
PLAYER2 = "player2"
COMPLETED = "completed"
WHITE_SYMBOL = "W"
BLACK_SYMBOL = "B"
END = "end turn"
ROSETTE = "rosette"
GAME_OVER = "game_over"


class RoyalGameOfUr:

    STARTING_PIECES = 7
    # these two are using to give a player a point if they complete a piece in order to determine when someone wins
    PLAYER1_SCORE = 0
    PLAYER2_SCORE = 0

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)
        self.player1 = None
        self.player2 = None
        self.black_entrance = None
        self.white_entrance = None
        # dictionary to keep track of players pieces
        self.player1_pieces = {}
        self.player2_pieces = {}
        self.piece = None
        self.piece2 = None

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        # these help me alternate turns between players player 1 runs while odd player 2 runs when even
        player1_turn = 1
        player2_turn = 1

        self.player1 = input("What is your name?")
        print(self.player1, "you will play as", WHITE)
        # this will create all of the pieces depending on what self.STARTING_PIECES value is
        self.create_pieces(self.STARTING_PIECES, PLAYER1)

        self.player2 = input("What is your name")
        print(self.player2, "you will play as", BLACK)
        self.create_pieces(self.STARTING_PIECES, PLAYER2)
        # this will find the entrance square for both colors
        self.find_entrance(self.board)
        # will run until either player gets all of their pieces complete
        while self.PLAYER1_SCORE < self.STARTING_PIECES and self.PLAYER2_SCORE < self.STARTING_PIECES:
            # loop for player1's turn
            while player1_turn % 2 != 0:
                # this list will help keep track of the available options the user can select
                option_list = []
                self.display_board()
                dice_roll = self.roll_d4_dice()

                print(self.player1, "you rolled a", dice_roll)
                # skips turn if the roll is 0 because no moves are possible
                if dice_roll == 0:
                    print("No moves are possible with the current dice roll.")
                    player1_turn += 1
                    player2_turn += 1

                else:
                    # displays available options
                    self.display_options(self.player1_pieces, self.STARTING_PIECES, dice_roll, option_list)
                    # if option_list is empty meaning no moves are possible then the next player will have their turn
                    if not option_list:
                        print("No moves are possible with the current dice roll.")
                        player1_turn += 1
                        player2_turn += 1

                    else:
                        which_move = int(input("Which move do you wish to make?"))
                        # if the user enters a number which is not a current option they will not be able to continue
                        # until they select a correct move
                        while which_move not in option_list:
                            print("That move is not available please reenter")
                            which_move = int(input("Which move do you wish to make?"))
                        # once they select a move that works this will move the piece
                        self.move_piece(dice_roll, self.player1_pieces[which_move])
                        # checks if player has won and will end the game
                        if self.PLAYER1_SCORE == self.STARTING_PIECES:
                            player1_turn += 1
                            print(self.player1, "has won the game!")

                        else:

                            print("No moves are possible with the current dice roll.")
                            player1_turn += 1
                            player2_turn += 1

            while player2_turn % 2 == 0:
                # this list will help keep track of the available options the user can select
                option_list = []
                self.display_board()
                dice_roll = self.roll_d4_dice()

                print(self.player2, "you rolled a", dice_roll)
                # skips turn if the roll is 0 because no moves are possible
                if dice_roll == 0:
                    print("No moves are possible with the current dice roll.")
                    player1_turn += 1
                    player2_turn += 1

                else:
                    # displays available options
                    self.display_options(self.player2_pieces, self.STARTING_PIECES, dice_roll, option_list)
                    # if option_list is empty meaning no moves are possible then the next player will have their turn
                    if not option_list:
                        print("No moves are possible with the current dice roll.")
                        player1_turn += 1
                        player2_turn += 1

                    else:
                        which_move = int(input("Which move do you wish to make?"))
                        # if the user enters a number which is not a current option they will not be able to continue
                        # until they select a correct move
                        while which_move not in option_list:
                            print("That move is not available please reenter")
                            which_move = int(input("Which move do you wish to make?"))
                        # once they select a move that works this will move the piece
                        self.move_piece(dice_roll, self.player2_pieces[which_move])
                        # checks if player has won and will end the game
                        if self.PLAYER2_SCORE == self.STARTING_PIECES:
                            player2_turn += 1
                            print(self.player2, "has won the game!")

                        else:
                            print("No moves are possible with the current dice roll.")
                            player1_turn += 1
                            player2_turn += 1

    # this function will create the pieces of both players, it will create pieces based off amount entered
    def create_pieces(self, number_of_pieces, player):
        # creates if its white
        if player == PLAYER1:
            for i in range(number_of_pieces):
                self.piece = UrPiece(WHITE, WHITE_SYMBOL + str(i))
                self.player1_pieces[i] = self.piece
        # creates if its black
        elif player == PLAYER2:
            for i in range(number_of_pieces):
                # creates a piece
                self.piece2 = UrPiece(BLACK, BLACK_SYMBOL + str(i))
                # sets the piece's key to the number piece it is
                self.player2_pieces[i] = self.piece2

    def display_options(self, pieces, number_of_moves, dice_roll, option_list):
        for i in range(number_of_moves):
            if pieces[i].color == WHITE:
                # if the piece is completed this will display
                if pieces[i].complete:
                    print(pieces[i].symbol, COMPLETED)
                # checks if piece can move
                elif pieces[i].can_move(dice_roll, self.white_entrance):
                    # if the move is possible then the move number will be appended to the list of options
                    option_list.append(i)
                    # if the position exist and isn't none then the cordinates it is on will display
                    if pieces[i].position:
                        print(i, pieces[i].symbol, pieces[i].position.position)
                        # if the position does not exist it is not on the board
                    if not pieces[i].position:
                        print(i, pieces[i].symbol, "currently off the board")
            # runs exactly like the white color loop just with self.black_entrance
            elif pieces[i].color == BLACK:
                if pieces[i].complete:
                    print(pieces[i].symbol, COMPLETED)
                elif pieces[i].can_move(dice_roll, self.black_entrance):
                    option_list.append(i)
                    if pieces[i].position:
                        print(i, pieces[i].symbol, pieces[i].position.position)
                    if not pieces[i].position:
                        print(i, pieces[i].symbol, "currently off the board")

    # this function will find the entrance square for both colors
    def find_entrance(self, board):
        for position in board:
            for i in range(len(position)):
                if position[i].entrance == WHITE:
                    # once found it sets these variables to there color's entrance square
                    self.white_entrance = position[i]
                elif position[i].entrance == BLACK:
                    self.black_entrance = position[i]

    # this function moves the piece that is entered in the parameters
    def move_piece(self, number_of_moves, piece):
        # if the piece is not on the board and the roll is a 1 it
        # will set it too whatever the pieces entrance position is
        if not piece.position and number_of_moves == 1 and piece.color == WHITE:
            piece.position = self.white_entrance
            piece.position.piece = piece

        elif not piece.position and number_of_moves == 1 and piece.color == BLACK:
            piece.position = self.black_entrance
            piece.position.piece = piece

        else:
            """
             if the piece is off the board and the roll is bigger then one it sets
             position to starting and then subtracts a move, 
             this causes one move spent moving onto the board
            """
            if not piece.position:
                if piece.color == WHITE:
                    piece.position = self.white_entrance
                    number_of_moves -= 1

                elif piece.color == BLACK:
                    piece.position = self.black_entrance
                    number_of_moves -= 1
            # sets the position before it starts moving
            start_position = piece.position

            # runs for number_of_moves left
            for i in range(number_of_moves):
                # if it passes exit and exits the board then the piece becomes completed
                if piece.position.exit:
                    piece.complete = True
                    piece.position = None
                    # once completed the player will get a point for completing
                    if piece.color == WHITE:
                        self.PLAYER1_SCORE += 1

                    elif piece.color == BLACK:
                        self.PLAYER2_SCORE += 1
                # if piece will move to the next square position depending on their color
                elif piece.color == WHITE:
                    piece.position = piece.position.next_white
                elif piece.color == BLACK:
                    piece.position = piece.position.next_black
            # if the piece does not have a position meaning it exited the board
            # then its starting position will be removed
            if not piece.position:
                if start_position:
                    start_position.piece = None
            else:
                # if the piece now exist it's old position is removed
                if piece.position.piece:
                    piece.position.piece.position = None
                # this is so the square they land on displays the piece
                piece.position.piece = piece
                # if start_position exist then it's new piece will be none
                # because the piece has been moved off of it
                if start_position:
                    start_position.piece = None


if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
