import datetime
import gym
from monte import mc_main
from td import td_main


if __name__ == "__main__":
    env = gym.make('Acrobot-v1')

    precision_for_discretization = 0

    num_episodes = 30000

    num_states_per_episode = 499

    discount_factor = 0.99

    # mc_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)
    td_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)
