import gym

from baselines import deepq
import gym_tic_tac_toe
import argparse
import sys

args = None

def main():
    env = gym.make("tic_tac_toe-v0")
    # act = deepq.load(args.load)

    act = deepq.learn(env, network='mlp', total_timesteps=0, load_path=args.load)

    # while True:
    total_reward = []
    for i in range(100):
        obs, done = env.reset(), False
        episode_rew = 0
        while not done:
            env.render("human")
            obs, rew, done, _ = env.step(act(obs[None], update_eps=0)[0])
            episode_rew += rew
        total_reward.append(episode_rew)
        env.render("human")
        print("Episode reward", episode_rew)
        print("-----------------------")
    print("total:", len(total_reward), ", Win: ", total_reward.count(1), ", Lost: ", total_reward.count(-1), ", Even: ", total_reward.count(0))
    print(total_reward)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--load', type=str, default="tictactoe_model.pkl", 
        help='load the model file')
    return parser.parse_args(argv)

if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    main()
