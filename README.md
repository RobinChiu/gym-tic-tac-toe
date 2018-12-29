# gym-tic-tac-toe

An example of a custom environment for https://github.com/openai/gym.

I want to try out self-play in a Reinforcement Learning context. Rather than the board game environments on openai/gym right now, which are "single-player" by providing a built-in opponent, I want to create an agent that learns a strategy by playing against itself, so it will try to maximize the reward for "player 1" and minimize it for "player 2".

The canonical example of a simple two player game is Tic Tac Toe, also known as Noughts and Crosses.

# 2018/11/08
Add the train_tictactoe.py and enjoy_tictactoe.py two files. Those base on the deepq of OPENAI baselines. 
You can run that command. It will train 100,000 Steps. 

    python train_tictactoe.py
  
Then you can run enjoy_tictactoe.py. You will get about 90% win rate. 

    python enjoy_tictactoe.py
  
![image](https://github.com/RobinChiu/gym-tic-tac-toe/blob/master/image/enjoy.png)
  
  
