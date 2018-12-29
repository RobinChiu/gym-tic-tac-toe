import gym
from gym import spaces
import numpy as np
import random

class Agent() :
    def __init__(self, player):
        self.player = player

    def whowin(self, board):
        result = 0
        data = [[0, 1, 2], [3, 4, 5], [6, 7, 8], 
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        for i, j, k in data:
            if board[i]!=0 and board[i]==board[j] and board[j]==board[k]:
                if board[i] == self.player:
                    result = 1
                else:
                    result = -1
        return result

    def isfinish(self, board):
        for i in board:
            if i == 0:
                return False;
        return True


    def minimax(self, board, flag):
        if self.whowin(board) == 1:
            return 1
        elif self.whowin(board) == -1:
            return -1
        elif self.isfinish(board):
            return 0
        
        result = []
        for i in range(9):
            if board[i] == 0:
                board[i] = flag
                result.append(self.minimax(board, -flag))
                board[i] = 0
        if flag==self.player:
            return max(result)
        else:
            return min(result) 

    def get_random(self):
        result = [i for i in range(9)]
        for i in range(9):
            j = random.randint(0, 8)
            temp = result[i]
            result[i] = result[j]
            result[j] = temp
        return result

    def next_pos(self, board):
        max_value = -10
        pos = -1
        post_list = self.get_random()
        for i in post_list:
            if board[i]==0:
                board[i]=self.player
                value = self.minimax(board, -self.player)
                board[i]=0
                if value > max_value:
                    max_value = value
                    pos = i
        return pos



class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(9)
        high = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        self.observation_space = spaces.Box(-high, high) # flattened
        self.agent = Agent(-1)
        self.use_agent = False

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
            if self.use_agent:
                pos = self.agent.next_pos(state["board"])
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
        if random.randint(0, 1) == 0:
            self.use_agent = False
        else:
            self.use_agent = True


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
                