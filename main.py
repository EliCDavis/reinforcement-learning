import datetime
import gym
from monte import mc_main


if __name__ == "__main__":
    env = gym.make('Acrobot-v1')

    precision_for_discretization = 2

    num_episodes = 300

    num_states_per_episode = 499

    discount_factor = 0.8

    mc_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)