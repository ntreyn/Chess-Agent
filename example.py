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
    move_options = env.get_moves()
    count = 0

    while True:
        env.render()
        count += 1
        print("Turn {}".format(count))
        
        print("{}, your turn".format(turn))
        while True:
            while True:
                piece = input("Choose piece: ")
                move = input("Choose move: ")
                if move != '':
                    break

            action = (piece.upper(), move.upper())

            if action not in move_options:
                print("Error: invalid action")
                continue
            else:
                break
        
        done, move_options, status = env.step(action)

        # End of turn
        if done:
            if status == 'W' or status == 'B':
                print("{} won!".format(turn_map[status]))
            else:
                print("Draw")
            env.render()
            break

        turn = turn_map[env.player]

    


if __name__ == "__main__":
    main()