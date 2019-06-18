import numpy as np 

class chess_env:

    """
    Board value mappings:
    
    0 : empty

    1 : white pawn
    2 : white rook
    3 : white horse
    4 : white bishop
    5 : white queen
    6 : white king

    -1 : black pawn
    -2 : black rook
    -3 : black horse
    -4 : black bishop
    -5 : black queen
    -6 : black king

    (0,0) -> top left corner
    """


    def __init__(self):
        self.state_size = 13 ** 64
        self.player = 'W'
        self.state_count = 0
        self.state_space = {}
    
    def reset(self):
        self.board = [
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 3, 4, 5, 6, 4, 3, 2]
        ]
        self.done = False
        pass 

    def step(self):
        pass

    def render(self):
        pass

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
