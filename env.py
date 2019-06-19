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
        self.player = 'W'
        self.state_count = 0
        self.state_space = {}
        self.reset()
    
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
        pass 

    def step(self):
        pass

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
