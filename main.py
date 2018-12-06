import datetime
import gym
from monte import mc_main
from sarsa import sarsa_main
from q import q_main


def big_fat_run():
    envs = ['Acrobot-v1', 'CartPole-v1', 'MountainCar-v0', 'MountainCarContinuous-v0', 'Pendulum-v0', 'BipedalWalker-v2'] 
    discs = [0, 1, 2]
    discounts = [.01, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99]
    for e in envs:
        for p in discs:
            for d in discounts:
                env = gym.make(e)
                n =  str(e) + " - " + str(p) + " - " + str(d) + datetime.datetime.now().strftime("%Y-%m-%d %H %M")
                q_main( "fat/q- " + n, env, 1000, 498, d, p)
                sarsa_main( "fat/sarsa- " + n, env, 1000, 498, d, p)
                
if __name__ == "__main__":

    # env = gym.make('Acrobot-v1')

    # precision_for_discretization = 0

    # num_episodes = 10000

    # num_states_per_episode = 498

    # discount_factor = 0.99

    # mc_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)
    # sarsa_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)
    # q_main( "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M"), env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization)

    big_fat_run()