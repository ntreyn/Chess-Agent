import numpy as np 

class chess_env:

    """
    (0,0) -> top left corner
    """
    
    piece_unicode = {
	    'p': "♙", 'r': "♖", 'n': "♘", 'b': "♗", 'k': "♔", 'q': "♕", 
	    'P': "♟", 'R': "♜", 'N': "♞", 'B': "♝", 'K': "♚", 'Q': "♛" ,
	    ' ': ' '
    }

    pieces_to_ids = {
        'R1': 1, 'N1': 2, 'B1': 3, 'Q': 4, 'K': 5, 'B2': 6, 'N2': 7, 'R2': 8,
        'P1': 9, 'P2': 10, 'P3': 11, 'P4': 12, 'P5': 13, 'P6': 14, 'P7': 15, 'P8': 16, 
        'r1': -1, 'n1': -2, 'b1': -3, 'q': -4, 'k': -5, 'b2': -6, 'n2': -7, 'r2': -8,
        'p1': -9, 'p2': -10, 'p3': -11, 'p4': -12, 'p5': -13, 'p6': -14, 'p7': -15, 'p8': -16, 
        ' ': 0
    }

    ids_to_pieces = {v: k for k, v in pieces_to_ids.items()}

    def __init__(self):
        self.state_size = 13 ** 64
        self.state_count = 0
        self.state_space = {}
        self.reset()
        self.set_piece_locations()
    
    def reset(self):
        self.board = [
            [-1, -2, -3, -4, -5, -6, -7, -8],
            [-9, -10, -11, -12, -13, -14, -15, -16],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [9, 10, 11, 12, 13, 14, 15, 16],
            [1, 2, 3, 4, 5, 6, 7, 8]
        ]
        self.done = False
        self.player = 'W'

    def step(self, action):
        """
        action : (piece, tile)
        piece : letter+number(optional)
        tile : letter+number -> (row, col)
        """
        piece = self.translate_piece(action[0])
        tile = self.translate_tile(action[1])






    def render(self):
        row_ids = [8,7,6,5,4,3,2,1]
        col_ids = ['A','B','C','D','E','F','G','H']
        row_ind = 0
        boundary = '  ' + '-' * 25
        print()
        print(boundary)
        
        for row in self.board:
            print(row_ids[row_ind], end=' ')
            row_ind += 1

            for tile in row:
                piece = self.ids_to_pieces[tile]
                img = self.piece_unicode[piece[0]]
                print('|{}'.format(img), end=' ')
            print('|')
            print(boundary)

        print('   ', end='')
        for col in col_ids:
            print(col, end='  ')
        print('\n')

    def get_state(self):

        state_list = []
        
        for row in self.board:
            for tile in row:
                state_list.append(tile)

        state = tuple(state_list), self.player

        if state in self.state_space:
            return self.state_space[state]
        else:
            self.state_space[state] = self.state_count
            self.state_count += 1
            return self.state_space[state]

    def set_piece_locations(self):
        self.piece_locations = {}

        for r, row in enumerate(self.board):
            for c, tile in enumerate(row):
                if tile != ' ':
                    self.piece_locations[tile] = (r, c)

    def translate_piece(self, piece):
        if self.player == 'W':
            return piece.upper()
        else:
            return piece.lower()

    def translate_tile(self, tile):
        letter = tile[0].upper()
        number = int(tile[1])

        letter_to_col = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7
        }

        row = 8 - number
        col = letter_to_col[letter]

        return (row, col)

    def can_capture(self, p1, p2):
        return p1.islower() != p2.islower()

    def in_bounds(self, r, c):
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        else:
            return True

    def step_checker(self, row_offset, col_offset, tile, piece):
        r, c = tile

        while True:
            r += row_offset
            c += col_offset

            if not self.in_bounds(r, c):
                break

            if self.board[r][c] == ' ':
                # Open square, possible move
                pass
            elif self.can_capture(piece, self.board[r][c]):
                # Enemy piece, possible move
                break
            else:
                # Friendly piece, impossible move
                break


    def num_attacking(self, tile):
        # Number of enemy pieces attacking square
        pass

    def num_defending(self, tile):
        # Number of friendly pieces defending square
        pass

    def pawn_actions(self, pawn):

        row, col = self.piece_locations[pawn]

        if pawn[0] == 'P':
            not_last = row != 0
            not_left_last = col != 0 and not_last
            not_right_last = col != 7 and not_last
            
            if row == 6 and self.board[5][col] == ' ' and self.board[4][col] == ' ':
                # Starting Double Move Forward
                pass
            if not_last and self.board[row - 1] == ' ':
                # Single Move Forward
                pass
            if not_left_last and self.can_capture(pawn, self.board[row - 1][col - 1]):
                # Diagonal capture left
                pass
            if not_right_last and self.can_capture(pawn, self.board[row - 1][col + 1]):
                # Diagonal capture right
                pass
            
            # En Passant
            # TODO

            if row == 1 and self.board[row - 1] == ' ':
                # Last Row Promotion
                pass

        elif pawn[0] == 'p':
            not_last = row != 7
            not_left_last = col != 0 and not_last
            not_right_last = col != 7 and not_last
            
            if row == 1 and self.board[2][col] == ' ' and self.board[3][col] == ' ':
                # Starting Double Move Forward
                pass
            if not_last and self.board[row + 1] == ' ':
                # Single Move Forward
                pass
            if not_left_last and self.can_capture(pawn, self.board[row + 1][col - 1]):
                # Diagonal capture left
                pass
            if not_right_last and self.can_capture(pawn, self.board[row + 1][col + 1]):
                # Diagonal capture right
                pass
            
            # En Passant
            # TODO

            if row == 6 and self.board[row + 1] == ' ':
                # Last Row Promotion
                pass
        
        else:
            # Should never happen
            pass


    def rook_actions(self, rook):

        rook_tile = self.piece_locations[rook]
        offsets = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]

        for r, c in offsets:
            self.step_checker(r, c, rook_tile, rook)

        # Castling
        # TODO


    def knight_actions(self, knight):
        """
            1       8
        2               7
                N       
        3               6
            4       5   
        """

        # 8 'L' Jumps

        row, col = self.piece_locations[knight]

        jumps = [
            (row - 1, col - 2), (row - 2, col - 1),
            (row - 1, col + 2), (row - 2, col + 1),
            (row + 1, col - 2), (row + 2, col - 1),
            (row + 1, col + 2), (row + 2, col + 1)
        ]

        for r, c in jumps:
            if self.in_bounds(r, c):
                tile = self.board[r][c]
                if tile == ' ' or self.can_capture(knight, tile):
                    # Possible move
                    pass


    def bishop_actions(self, bishop):

        bish_tile = self.piece_locations[bishop]
        offsets = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for r, c in offsets:
            self.step_checker(r, c, bish_tile, bishop)

    def queen_actions(self, queen):

        queen_tile = self.piece_locations[queen]
        offsets = [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for r, c in offsets:
            self.step_checker(r, c, queen_tile, queen)

    def king_actions(self, king):

        row, col = self.piece_locations[king]

        moves = [
            (row - 1, col - 1), (row + 1, col + 1),
            (row - 1, col + 1), (row + 1, col - 1),
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1)
        ]

        for r, c in moves:
            if self.in_bounds(r, c):
                tile = self.board[r][c]
                if self.num_attacking((r,c)) == 0 and (tile == ' ' or self.can_capture(king, tile)):
                    # Possible move
                    pass

        

