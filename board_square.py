"""
File: board_square.py
Author: Amarjot Gill
Date: 10/31/2020
Lab Section: 44
Email:  agill3@umbc.edu
Description:  This program is classes that using the can_move
should return True is the piece if able to move and
False if it is not able to move.
"""

WHITE = "White"
BLACK = "Black"


class UrPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol

    def can_move(self, num_moves, entrance):
        can_move = True
        current_position = None
        # if position is not on the board it will be set to the entrance position
        if not self.position:
            current_position = entrance
            num_moves -= 1
        else:
            current_position = self.position
        # loop to help determine where the landing position is
        # also will check if its an exit or not
        for i in range(num_moves):

            if can_move and current_position.exit and i + 1 == num_moves:
                current_position = None
            # if the number of moves is not exactly enough for one off the exit
            # you can't make the move
            elif can_move and current_position.exit and i + 1 < num_moves:
                return False

            elif can_move and self.color == WHITE:
                current_position = current_position.next_white

            elif can_move and self.color == BLACK:
                current_position = current_position.next_black

        # if the position is off the board then it was reached an exit
        if not current_position:
            return can_move

        else:

            if current_position.piece:
                # if its the same color has the piece then you can not make the move
                if current_position.piece.color == self.color:
                    can_move = False
                else:
                    can_move = True

            if current_position.piece:
                # if the piece on the position is a rosette then you can not move to it
                if current_position.rosette:
                    can_move = False

            return can_move


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
