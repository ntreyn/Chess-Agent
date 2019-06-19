#!/usr/bin/env python

from env import chess_env

import time

def main():
    env = chess_env()
    env.render()
    action = ('Q', 'c8')
    env.step(action)


if __name__ == "__main__":
    main()