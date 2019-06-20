#!/usr/bin/env python

from env import chess_env

import time

def main():
    env = chess_env()

    turn_map = {
        'W': 'White',
        'B': 'Black'
    }
    done = False
    turn = turn_map[env.player]

    while True:
        env.render()
        
        print("{}, your turn".format(turn))
        while True:
            while True:
                piece = input("Choose piece: ")
                move = input("Choose move: ")
                if move != '':
                    break

            move_options = env.get_moves()
            action = (piece.upper(), move.upper())

            if action not in move_options:
                print("Error: invalid action")
                continue
            else:
                break
        
        done = env.step(action)



        # End of turn
        if done:
            break

        turn = turn_map[env.player]

    


if __name__ == "__main__":
    main()