import numpy as np 
import copy
import random

class chess_env:

    """
    (0,0) -> top left corner
    """
    
    piece_unicode = {
	    'p': "♙", 'r': "♖", 'n': "♘", 'b': "♗", 'k': "♔", 'q': "♕", 
	    'P': "♟", 'R': "♜", 'N': "♞", 'B': "♝", 'K': "♚", 'Q': "♛" ,
	    ' ': ' '
    }

    def __init__(self):
        self.state_size = 13 ** 64
        self.action_size = 64 * 27
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

        self.pieces_to_ids = {
            'R1': 1, 'N1': 2, 'B1': 3, 'Q': 4, 'K': 5, 'B2': 6, 'N2': 7, 'R2': 8,
            'P1': 9, 'P2': 10, 'P3': 11, 'P4': 12, 'P5': 13, 'P6': 14, 'P7': 15, 'P8': 16, 
            'r1': -1, 'n1': -2, 'b1': -3, 'q': -4, 'k': -5, 'b2': -6, 'n2': -7, 'r2': -8,
            'p1': -9, 'p2': -10, 'p3': -11, 'p4': -12, 'p5': -13, 'p6': -14, 'p7': -15, 'p8': -16, 
            ' ': 0, 'C': 17, 'c': -17
        }

        self.ids_to_pieces = {v: k for k, v in self.pieces_to_ids.items()}

        self.state_visited = {}
        self.done = False
        self.player = 'W'
        self.black_remaining = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16]
        self.black_lost = []
        self.white_remaining = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.white_lost = []
        self.kings_moved = { 'W': False, 'B': False }
        self.rooks_moved = { 'W': [False, False], 'B': [False, False] }
        self.last_move = (0, (-1, -1))
        self.last_move_pawn_jump = False
        self.white_num_promotions = 1
        self.black_num_promotions = 1
        self.white_promotion_id = 18
        self.black_promotion_id = -18

        return self.get_state()


    def step(self, action):
        """
        action : (piece, tile)
        piece : letter+number(optional)
        tile : letter+number -> (row, col)
        """
        piece = self.correct_piece(action[0])
        piece = self.pieces_to_ids[piece]
        tile = self.tile_to_coord(action[1])

        reward = self.get_reward(piece, tile)

        self.execute_move(piece, tile)







        # End of step
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

        next_moves = self.get_moves()
        status = 'P'

        if not next_moves:
            if self.player == 'W':
                king_tile = self.piece_locations[5]
            else:
                king_tile = self.piece_locations[-5]

            check_num = self.num_attacking(king_tile)
            if check_num > 0:
                # Checkmate
                self.done = True
                if self.player == 'W':
                    status = 'B'
                else:
                    status = 'W'
            else:
                # Stalemate
                self.done = True
                status = 'D'
        
        state = self.get_state()
        if self.state_visited[state] >= 3 and status == 'P':
            self.done = True
            status = 'D'

        return state, reward, self.done, next_moves, status

    def execute_move(self, piece, tile):
        r, c = tile
        self.last_move_pawn_jump = False

        if abs(piece) == 5 or abs(piece) == 1 or abs(piece) == 8:
            if piece == 5:
                self.kings_moved['W'] = True
            elif piece == -5:
                self.kings_moved['B'] = True
            elif piece == 1:
                self.rooks_moved['W'][0] = True
            elif piece == 8:
                self.rooks_moved['W'][1] = True
            elif piece == -1:
                self.rooks_moved['B'][0] = True
            elif piece == -8:
                self.rooks_moved['B'][1] = True
            
        # Castling edge case
        if abs(piece) == 17:
            if piece > 0:
                # White
                rook_mult = 1
                king = 5
            else:
                # Black 
                rook_mult = -1
                king = -5

            if c == 2:
                # Queen's side
                rook_tile = (r, c + 1)
                rook = 1 * rook_mult
            else:
                # King's side
                rook_tile = (r, c - 1)
                rook = 8 * rook_mult

            rook_or_r, rook_or_c = self.piece_locations[rook]
            king_or_r, king_or_c = self.piece_locations[king]

            self.board[rook_or_r][rook_or_c] = 0
            self.board[king_or_r][king_or_c] = 0
            self.piece_locations[king] = tile
            self.piece_locations[rook] = rook_tile
            self.board[r][c] = king
            self.board[rook_tile[0]][rook_tile[1]] = rook

        elif self.board[r][c] == 0:
            or_r, or_c = self.piece_locations[piece]
            abs_p = abs(piece)
            
            # Pawn edge cases
            if abs_p >= 9 and abs_p <= 16:

                # Promotion edge case 
                if piece > 0:
                    last_row = 0
                    letter = 'Q'
                else:
                    last_row = 7
                    letter = 'q'
                
                if r == last_row and not self.checking_no_promotion:
                    
                    if piece > 0:
                        piece_name = letter + str(self.white_num_promotions)
                        piece_id = self.white_promotion_id
                        self.white_remaining.append(piece_id)
                        self.white_remaining.remove(piece)
                        self.white_num_promotions += 1
                        self.white_promotion_id += 1
                    else:
                        piece_name = letter + str(self.black_num_promotions)
                        piece_id = self.black_promotion_id
                        self.black_remaining.append(piece_id)
                        self.black_remaining.remove(piece)
                        self.black_num_promotions += 1
                        self.black_promotion_id -= 1

                    self.pieces_to_ids[piece_name] = piece_id
                    self.ids_to_pieces[piece_id] = piece_name
                    self.piece_locations[piece] = (-1, -1) 
                    piece = piece_id
                    
                    print(piece)
                    print(piece_name)

                # Set last_move_pawn_jump for en passant
                if abs(or_r - r) == 2:
                    self.last_move_pawn_jump = True
                # Execute en passant
                if or_c != c:
                    # new column, old row
                    opp_pawn = self.board[or_r][c]
                    self.piece_locations[opp_pawn] = (-1, -1)
                    self.board[or_r][c] = 0
                    if opp_pawn > 0:
                        self.white_remaining.remove(opp_pawn)
                        self.white_lost.append(opp_pawn)
                    else:
                        self.black_remaining.remove(opp_pawn)
                        self.black_lost.append(opp_pawn)
            
            self.board[or_r][or_c] = 0
            self.piece_locations[piece] = tile
            self.board[r][c] = piece
        
        else:
            or_r, or_c = self.piece_locations[piece]
            self.board[or_r][or_c] = 0
            opp_piece = self.board[r][c]
            self.piece_locations[opp_piece] = (-1, -1)

            if opp_piece > 0:
                self.white_remaining.remove(opp_piece)
                self.white_lost.append(opp_piece)
            else:
                self.black_remaining.remove(opp_piece)
                self.black_lost.append(opp_piece)

            # Promotion edge case
            if abs(piece) >= 9 and abs(piece) <= 16:  
                if piece > 0:
                    last_row = 0
                    letter = 'Q'
                else:
                    last_row = 7
                    letter = 'q'
                
                if r == last_row and not self.checking_no_promotion:
                    
                    if piece > 0:
                        piece_name = letter + str(self.white_num_promotions)
                        piece_id = self.white_promotion_id
                        self.white_remaining.append(piece_id)
                        self.white_remaining.remove(piece)
                        self.white_num_promotions += 1
                        self.white_promotion_id += 1
                    else:
                        piece_name = letter + str(self.black_num_promotions)
                        piece_id = self.black_promotion_id
                        self.black_remaining.append(piece_id)
                        self.black_remaining.remove(piece)
                        self.black_num_promotions += 1
                        self.black_promotion_id -= 1

                    self.pieces_to_ids[piece_name] = piece_id
                    self.ids_to_pieces[piece_id] = piece_name
                    self.piece_locations[piece] = (-1, -1) 
                    piece = piece_id
                    
                    print(piece)
                    print(piece_name)

            self.piece_locations[piece] = tile
            self.board[r][c] = piece


        self.last_move = piece, tile

    def render(self):
        row_ids = [8,7,6,5,4,3,2,1]
        col_ids = ['A','B','C','D','E','F','G','H']
        row_ind = 0
        boundary = '  ' + '-' * 25

        print()
        print("White taken: ", end='')
        for p in self.white_lost:
            piece = self.ids_to_pieces[p]
            img = self.piece_unicode[piece[0]]
            print(img, end=' ')

        
        print()
        print("Black taken: ", end='')
        for p in self.black_lost:
            piece = self.ids_to_pieces[p]
            img = self.piece_unicode[piece[0]]
            print(img, end=' ')

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
            temp_state = self.state_space[state]
            self.state_visited[temp_state] += 1
            return temp_state
        else:
            self.state_space[state] = self.state_count
            self.state_visited[self.state_count] = 1
            self.state_count += 1
            return self.state_space[state]

    def sample_action(self):
        return random.choice(self.get_moves())

    def get_reward(self, piece, tile):
    
        """
        Potential actions to reward:

        Attacking pieces
            -> Reward more for higher value pieces
        Defending pieces
            -> Reward more for higher value pieces
        Capturing pieces
            -> Reward more for higher value pieces

        Board coverage (some sort of area function)
        Attacking squares ???
            -> Rewards bishop/rook/queen/knight coverage
            -> Might tie into board coverage
                -> Number of squares attacking?
                -> Coverage function combining territory + squares attacking
                    -> Territoy meaning board "behind" pieces

        Checkmate
        Castling

        
        Promoting pieces
        
        Pawn wall / pawn solidity???
            -> Pawns arranged near king?

        Penalize for opponent's reward


        """

        return 0

    def move_to_action(self, piece, move):
        r, c = move
        return 64 * (abs(piece) - 1) + (r * 8 + c)

    def action_to_move(self, action):
        square = action % 64
        column = square % 8
        row = (square - column) // 8
        piece = (action - square) // 64 + 1
        if self.player == 'B':
            piece = piece * -1
        return piece, (int(row), int(column))

    def convert_action(self, action):
        piece_id, (r, c) = self.action_to_move(action)
        piece = self.ids_to_pieces[piece_id]
        tile = self.coord_to_tile(r, c)
        return piece, tile

    def set_piece_locations(self):
        self.piece_locations = {}

        for r, row in enumerate(self.board):
            for c, tile in enumerate(row):
                if tile != 0:
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
        if self.player == 'W':
            pieces = self.black_remaining
        else:
            pieces = self.white_remaining

        moves = []

        for p in pieces:
            abs_p = abs(p)
            if abs_p >= 9 and abs_p <= 16:
                pawn_moves = self.pawn_attacks(p)
                for m in pawn_moves:
                    moves.append(m)
            elif abs_p == 1 or abs_p == 8:
                rook_moves = self.rook_actions(p)
                for m in rook_moves:
                    moves.append(m)
            elif abs_p == 2 or abs_p == 7:
                knight_moves = self.knight_actions(p)
                for m in knight_moves:
                    moves.append(m)
            elif abs_p == 3 or abs_p == 6:
                bishop_moves = self.bishop_actions(p)
                for m in bishop_moves:
                    moves.append(m)
            elif abs_p == 4 or abs_p >= 18:
                queen_moves = self.queen_actions(p)
                for m in queen_moves:
                    moves.append(m)
            elif abs_p == 5:
                king_moves = self.king_attacking(p)
                for m in king_moves:
                    moves.append(m)
        
        num_attackers = 0

        for m in moves:
            if m == tile:
                num_attackers += 1
        
        return num_attackers

    def num_defending(self, tile):
        # Number of friendly pieces defending square
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'
        
        num_defenders = self.num_attacking(tile)

        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'
        
        return num_defenders

    def get_moves(self):
        raw_moves = self.potential_moves()
        moves = []

        for p, c in raw_moves:
            tile = self.coord_to_tile(c[0], c[1])
            piece = self.ids_to_pieces[p]
            moves.append((piece.upper(), tile))
        
        return moves

    def get_actions(self):
        raw_moves = self.potential_moves()
        actions = [self.move_to_action(p, c) for p, c in raw_moves]
        return actions

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
                p = -17
            else:
                p = 17
            moves.append((p, m))

        for p in pieces:
            abs_p = abs(p)
            if abs_p >= 9 and abs_p <= 16:
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
            elif abs_p == 4 or abs_p >= 18:
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

        if self.player == 'B':
            king = -5
        else:
            king = 5

        valid_moves = self.check_moves(moves, king)

        return valid_moves

    def check_moves(self, moves, king):
        temp_board = copy.deepcopy(self.board)
        temp_piece_locations = copy.deepcopy(self.piece_locations)
        temp_white_remaining = copy.deepcopy(self.white_remaining)
        temp_white_lost = copy.deepcopy(self.white_lost)
        temp_black_remaining = copy.deepcopy(self.black_remaining)
        temp_black_lost = copy.deepcopy(self.black_lost)
        temp_last_move = copy.deepcopy(self.last_move)

        valid_moves = []
        self.checking_no_promotion = True

        for piece, tile in moves:
            self.execute_move(piece, tile)
            king_tile = self.piece_locations[king]
            check_count = self.num_attacking(king_tile)

            if check_count == 0:
                valid_moves.append((piece, tile))

            self.board = copy.deepcopy(temp_board)
            self.piece_locations = copy.deepcopy(temp_piece_locations)
            self.white_remaining = copy.deepcopy(temp_white_remaining)
            self.white_lost = copy.deepcopy(temp_white_lost)
            self.black_remaining = copy.deepcopy(temp_black_remaining)
            self.black_lost = copy.deepcopy(temp_black_lost)
            self.last_move = copy.deepcopy(temp_last_move)
        
        self.checking_no_promotion = False
        return valid_moves

    def pawn_actions(self, pawn):

        row, col = self.piece_locations[pawn]
        moves = []

        if pawn > 0:
            not_last = row != 0
            not_left = col != 0
            not_right = col != 7
            
            if row == 6 and self.board[5][col] == 0 and self.board[4][col] == 0:
                # Starting Double Move Forward
                moves.append((4, col))
            if not_last and self.board[row - 1][col] == 0:
                # Single Move Forward
                moves.append((row - 1, col))
            if not_last and not_left and self.can_capture(pawn, self.board[row - 1][col - 1]):
                # Diagonal capture left
                moves.append((row - 1, col - 1))
            if not_last and not_right and self.can_capture(pawn, self.board[row - 1][col + 1]):
                # Diagonal capture right
                moves.append((row - 1, col + 1))
            if self.last_move_pawn_jump:
                lr, lc = self.last_move[1]
                if lr == row:
                    if lc + 1 == col or lc - 1 == col:
                        # En Passant
                        moves.append((row - 1, lc))
            if row == 1 and self.board[row - 1][col] == 0:
                # Last Row Promotion
                # TODO
                pass

        elif pawn < 0:
            not_last = row != 7
            not_left = col != 0
            not_right = col != 7
            
            if row == 1 and self.board[2][col] == 0 and self.board[3][col] == 0:
                # Starting Double Move Forward
                moves.append((3, col))
            if not_last and self.board[row + 1][col] == 0:
                # Single Move Forward
                moves.append((row + 1, col))
            if not_last and not_left and self.can_capture(pawn, self.board[row + 1][col - 1]):
                # Diagonal capture left
                moves.append((row + 1, col - 1))
            if not_last and not_right and self.can_capture(pawn, self.board[row + 1][col + 1]):
                # Diagonal capture right
                moves.append((row + 1, col + 1))
            if self.last_move_pawn_jump:
                lr, lc = self.last_move[1]
                if lr == row:
                    if lc + 1 == col or lc - 1 == col:
                        # En Passant
                        moves.append((row + 1, lc))
            if row == 6 and self.board[row + 1][col] == 0:
                # Last Row Promotion
                # TODO
                pass
        
        else:
            # Should never happen
            pass

        return moves

    def pawn_attacks(self, pawn):
        row, col = self.piece_locations[pawn]
        moves = []

        if pawn > 0:
            not_last = row != 0
            not_left = col != 0
            not_right = col != 7

            if not_last and not_left and self.can_capture(pawn, self.board[row - 1][col - 1]):
                # Diagonal capture left
                moves.append((row - 1, col - 1))
            if not_last and not_right and self.can_capture(pawn, self.board[row - 1][col + 1]):
                # Diagonal capture right
                moves.append((row - 1, col + 1))
            if self.last_move_pawn_jump:
                lr, lc = self.last_move[1]
                if lr == row:
                    if lc + 1 == col or lc - 1 == col:
                        # En Passant
                        moves.append((row - 1, lc))

        elif pawn < 0:
            not_last = row != 7
            not_left = col != 0
            not_right = col != 7
            
            if not_last and not_left and self.can_capture(pawn, self.board[row + 1][col - 1]):
                # Diagonal capture left
                moves.append((row + 1, col - 1))
            if not_last and not_right and self.can_capture(pawn, self.board[row + 1][col + 1]):
                # Diagonal capture right
                moves.append((row + 1, col + 1))
            if self.last_move_pawn_jump:
                lr, lc = self.last_move[1]
                if lr == row:
                    if lc + 1 == col or lc - 1 == col:
                        # En Passant
                        moves.append((row + 1, lc))
 
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

    def king_attacking(self, king):
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

