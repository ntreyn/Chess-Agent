import numpy as np 
import random

class human_agent():
    def __init__(self, c):
        self.color = c

    def turn(self, move_options):
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
        return piece, move


class rl_agent():
    def __init__(self, c, e):
        self.color = c
        self.env = e

    def turn(self, move_options):
        return self.env.sample_action()