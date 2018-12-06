import gym
import numpy as np
from numpy import sin, cos, pi

if __name__ == "__main__":
    env = gym.make('Acrobot-v1')

    precision_for_discretization = 0

    num_episodes = 100000

    num_states_per_episode = 499

    print(env)
    print(dir(env))
    print(vars(env))

    discount_factor = 0.99
    env.reset()
    for x in range(1000):
        v =(pi/1000) * x *2
        env.env.state = [v, 0, 0, 0]
        print(env.env._get_ob())
        print(v)
        env.render()
        
