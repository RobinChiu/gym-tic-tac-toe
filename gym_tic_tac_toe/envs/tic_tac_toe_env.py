import gym
from gym import spaces
import numpy as np
import random

class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(9)
        high = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        self.observation_space = spaces.Box(-high, high) # flattened

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        state, reward, done, others = self._step1([1, action])

        #check if it's done
        if not done:
            # empty pos
            empty_pos = [i for i, j in enumerate(state["board"]) if j == 0]
            # print(empty_pos)
            pos = random.choice(empty_pos)
            state, reward, done, others =  self._step1([-1, pos])

        return np.array(state["board"]), reward, done, others

    def _step1(self, action):
        done = False
        reward = 0

        p, square = action
        
       # p = p*2 - 1
        # check move legality
        board = self.state['board']
        proposed = board[square]
        om = self.state['on_move']
        if (proposed != 0):  # wrong player, not empty
            print("illegal move ", action, ". (square occupied): ", square)
            done = True
            reward = -1 * om  # player who did NOT make the illegal move
        elif (p != om):  # wrong player, not empty
            print("illegal move  ", action, " not on move: ", p)
            done = True
            reward = -1 * om  # player who did NOT make the illegal move
        else:
            board[square] = p
            self.state['on_move'] = -p

        # check game over
        for i in range(3):
            # horizontals and verticals
            if ((board[i * 3] == p and board[i * 3 + 1] == p and board[i * 3 + 2] == p)
                or (board[i + 0] == p and board[i + 3] == p and board[i + 6] == p)):
                reward = p
                done = True
                break
        # diagonals
        if((board[0] == p and board[4] == p and board[8] == p)
            or (board[2] == p and board[4] == p and board[6] == p)):
                reward = p
                done = True

        if 0 not in board:
            done = True
                
        return self.state, float(reward), done, {}
    def _reset(self):
        self.state = {}
        self.state['board'] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.state['on_move'] = 1
        return np.array(self.state["board"])
    def _render(self, mode='human', close=False):
        if close:
            return
        print("on move: " , self.state['on_move'])
        for i in range (9):
            if i != 0 and i % 3 == 0:
                print("")
            print ("%2d"%(self.state['board'][i]), end=" ")
        print()
    def move_generator(self):
        moves = []
        for i in range (9):
            
            if (self.state['board'][i] == 0):
                p = self.state['on_move']
                m = [p, i]
                moves.append(m)
        return moves
                