#!/usr/bin/env python

from env import chess_env
from agent import human_agent, rl_agent
from learner import learner

class play_game:
    def __init__(self):
        self.env = chess_env()
        self.learner = learner(self.env)
        self.learner.learn()

    def play(self):

        turn_map = {
            'W': 'White',
            'B': 'Black'
        }
        done = False
        turn = self.env.player
        move_options = self.env.get_moves()
        count = 0
        # state = self.env.get_state()
        
        while True:
            count += 1
            print("Turn {}".format(count))
            self.env.render()
            print("{}, your turn".format(turn_map[turn]))

            if turn == 'W':
                action = self.white.turn(move_options)
            else:
                action = self.black.turn(move_options)
            
            _, _, done, move_options, status = self.env.step(action)
             # new_state, reward, done, move_options, status = self.env.step(action)

            # End of turn
            if done:
                break
            
            # state = new_state
            turn = self.env.player

        self.env.render()
        self.env.reset()
        print("Gameover")

        if status == 'W' or status == 'B':
            print("{} won!".format(turn_map[status]))
        else:
            print("Draw")

    def mode(self):
        while True:
            print("Pick a mode: \n(1) Human vs. Human\n(2) Human vs. Computer\n(3) Computer vs. Computer")
            mode = input()

            if mode == '1':
                self.white = human_agent('W')
                self.black = human_agent('B')

            elif mode == '2':
                while True:
                    side = input("Choose your side (W / B): ")
                    if side == 'W':
                        self.white = human_agent('W')
                        self.black = rl_agent('B', self.env)
                        break
                    elif side == 'B':
                        self.black = human_agent('B')
                        self.white = rl_agent('W', self.env)
                        break
                    else:
                        print("Invalid side, please try again")
                        continue
                

            elif mode == '3':
                self.white = rl_agent('W', self.env)
                self.black = rl_agent('B', self.env)

            else:
                print("Invalid mode, please try again")
                continue
            break

def main():
    game = play_game()

    while True:
        game.mode()
        game.play()
        temp = input("Would you like to play again? (y/n) ")
        if temp == 'n':
            break
    

if __name__ == "__main__":
    main()