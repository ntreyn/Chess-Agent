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
        ' ': 0, 'C': 17, 'c': -17
    }

    """
    (+/-) 17 : Castle
    """

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
        self.black_remaining = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16]
        self.black_lost = []
        self.white_remaining = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.white_lost = []
        self.kings_moved = { 'W': False, 'B': False }
        self.rooks_moved = { 'W': [False, False], 'B': [False, False] }

    def step(self, action):
        """
        action : (piece, tile)
        piece : letter+number(optional)
        tile : letter+number -> (row, col)
        """
        piece = self.correct_piece(action[0])
        tile = self.tile_to_coord(action[1])

        print(self.get_moves())






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

    def correct_piece(self, piece):
        if self.player == 'W':
            return piece.upper()
        else:
            return piece.lower()

    def tile_to_coord(self, tile):
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

    def coord_to_tile(self, r, c):
        col_to_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        letter = col_to_letter[c]
        number = 8 - r
        return letter + str(number)    

    def can_capture(self, p1, p2):
        prod = p1 * p2
        if prod < 0:
            return True
        else:
            return False

    def in_bounds(self, r, c):
        if r > 7 or r < 0 or c > 7 or c < 0:
            return False
        else:
            return True

    def step_checker(self, row_offset, col_offset, tile, piece):
        r, c = tile
        moves = []

        while True:
            r += row_offset
            c += col_offset

            if not self.in_bounds(r, c):
                break

            if self.board[r][c] == 0:
                # Open square, possible move
                moves.append((r, c))
                
            elif self.can_capture(piece, self.board[r][c]):
                # Enemy piece, possible move
                moves.append((r, c))
                break
            else:
                # Friendly piece, impossible move
                break
        
        return moves

    def num_attacking(self, tile):
        # Number of enemy pieces attacking square
        pass

    def num_defending(self, tile):
        # Number of friendly pieces defending square
        pass

    def get_moves(self):
        raw_moves = self.potential_moves()
        moves = []

        for p, c in raw_moves:
            tile = self.coord_to_tile(c[0], c[1])
            piece = self.ids_to_pieces[p]
            moves.append((piece, tile))
        
        return moves

    def potential_moves(self):
        if self.player == 'W':
            pieces = self.white_remaining
        else:
            pieces = self.black_remaining

        moves = []
        castle_moves = self.castling_actions()
        for m in castle_moves:
            r, _ = m
            if r == 0:
                mult = -1
            else:
                mult = 1
            p = 17 * mult
            moves.append((p, m))

        for p in pieces:
            if abs_p >= 9:
                pawn_moves = self.pawn_actions(p)
                for m in pawn_moves:
                    moves.append((p, m))
            elif abs_p == 1 or abs_p == 8:
                rook_moves = self.rook_actions(p)
                for m in rook_moves:
                    moves.append((p, m))
            elif abs_p == 2 or abs_p == 7:
                knight_moves = self.knight_actions(p)
                for m in knight_moves:
                    moves.append((p, m))
            elif abs_p == 3 or abs_p == 6:
                bishop_moves = self.bishop_actions(p)
                for m in bishop_moves:
                    moves.append((p, m))
            elif abs_p == 4:
                queen_moves = self.queen_actions(p)
                for m in queen_moves:
                    moves.append((p, m))
            elif abs_p == 5:
                king_moves = self.king_actions(p)
                for m in king_moves:
                    moves.append((p, m))
            else:
                # Should never happen
                pass
    
        return moves

    def pawn_actions(self, pawn):

        row, col = self.piece_locations[pawn]
        moves = []

        if pawn > 0:
            not_last = row != 0
            not_left_last = col != 0 and not_last
            not_right_last = col != 7 and not_last
            
            if row == 6 and self.board[5][col] == 0 and self.board[4][col] == 0:
                # Starting Double Move Forward
                moves.append((4, col))
            if not_last and self.board[row - 1][col] == 0:
                # Single Move Forward
                moves.append((row - 1, col))
            if not_left_last and self.can_capture(pawn, self.board[row - 1][col - 1]):
                # Diagonal capture left
                moves.append((row - 1, col - 1))
            if not_right_last and self.can_capture(pawn, self.board[row - 1][col + 1]):
                # Diagonal capture right
                moves.append((row - 1, col + 1))
            
            # En Passant
            # TODO

            if row == 1 and self.board[row - 1][col] == 0:
                # Last Row Promotion
                # TODO
                pass

        elif pawn < 0:
            not_last = row != 7
            not_left_last = col != 0 and not_last
            not_right_last = col != 7 and not_last
            
            if row == 1 and self.board[2][col] == 0 and self.board[3][col] == 0:
                # Starting Double Move Forward
                moves.append((3, col))
            if not_last and self.board[row + 1][col] == 0:
                # Single Move Forward
                moves.append((row + 1, col))
            if not_left_last and self.can_capture(pawn, self.board[row + 1][col - 1]):
                # Diagonal capture left
                moves.append((row + 1, col - 1))
            if not_right_last and self.can_capture(pawn, self.board[row + 1][col + 1]):
                # Diagonal capture right
                moves.append((row + 1, col + 1))
            
            # En Passant
            # TODO

            if row == 6 and self.board[row + 1][col] == 0:
                # Last Row Promotion
                # TODO
                pass
        
        else:
            # Should never happen
            pass

        return moves

    def rook_actions(self, rook):

        rook_tile = self.piece_locations[rook]
        offsets = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]
        moves = []

        for r, c in offsets:
            steps = self.step_checker(r, c, rook_tile, rook)
            for s in steps:
                moves.append(s)

        return moves

    def knight_actions(self, knight):
        """
            1       8
        2               7
                N       
        3               6
            4       5   
        """

        row, col = self.piece_locations[knight]
        jumps = [
            (row - 1, col - 2), (row - 2, col - 1),
            (row - 1, col + 2), (row - 2, col + 1),
            (row + 1, col - 2), (row + 2, col - 1),
            (row + 1, col + 2), (row + 2, col + 1)
        ]
        moves = []

        for r, c in jumps:
            if self.in_bounds(r, c):
                tile = self.board[r][c]
                if tile == 0 or self.can_capture(knight, tile):
                    # Possible move
                    moves.append((r, c))
        
        return moves

    def bishop_actions(self, bishop):

        bish_tile = self.piece_locations[bishop]
        offsets = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        moves = []

        for r, c in offsets:
            steps = self.step_checker(r, c, bish_tile, bishop)
            for s in steps:
                moves.append(s)

        return moves

    def queen_actions(self, queen):

        queen_tile = self.piece_locations[queen]
        offsets = [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        moves = []

        for r, c in offsets:
            steps = self.step_checker(r, c, queen_tile, queen)
            for s in steps:
                moves.append(s)

        return moves

    def king_actions(self, king):

        row, col = self.piece_locations[king]
        spaces = [
            (row - 1, col - 1), (row + 1, col + 1),
            (row - 1, col + 1), (row + 1, col - 1),
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1)
        ]
        moves = []

        for r, c in spaces:
            if self.in_bounds(r, c):
                tile = self.board[r][c]
                if self.num_attacking((r,c)) == 0 and (tile == 0 or self.can_capture(king, tile)):
                    # Possible move
                    moves.append((r, c))
        
        return moves

    def castling_actions(self):
        moves = []
        if self.player == 'W':
            row = 7
        else:
            row = 0

        if not self.kings_moved[self.player]:
            if self.num_attacking((row, 4)) > 0:
                return moves

            if not self.rooks_moved[self.player][0]:
                # Queen side
                cols = [1, 2, 3]
                good = True

                for c in cols:
                    if c != 1:
                        # Check attacked
                        if self.num_attacking((row, c)) > 0:
                            good = False
                    # Check filled
                    if self.board[row][c] != 0:
                        good = False
        
                if good:
                    moves.append((row, 2))

            if not self.rooks_moved[self.player][1]:
                # King side
                cols = [5, 6]
                good = True

                for c in cols:
                    # Check attacked
                    if self.num_attacking((row, c)) > 0:
                        good = False
                    # Check filled
                    if self.board[row][c] != 0:
                        good = False

                if good:
                    moves.append((row, 6))

        return moves

