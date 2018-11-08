import gym

from baselines import deepq
import gym_tic_tac_toe


def callback(lcl, glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved


def main():
    env = gym.make("tic_tac_toe-v0")
    model = deepq.models.mlp([64])
    act = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback
    )
    print("Saving model to tictactoe_model.pkl")
    act.save("tictactoe_model.pkl")

if __name__ == '__main__':
    main()
