from util import *
from decision import Decision
import gym
env = gym.make('Acrobot-v1')

"""
    Notes....
    Action 2 moves to the left..
    Action 0 moves to the right..
    Action 1 moves.....?

    basic reward:
        Trials:
            precision_for_discretization = 1
            num_episodes = 10000
            num_states_per_episode = 100
            succeeded after: never

        Trials:
            precision_for_discretization = 1
            num_episodes = 100000
            num_states_per_episode = 100
            succeeded after: ?

"""

precision_for_discretization = 3

num_episodes = 1000

num_states_per_episode = 499

def mc_main():

    print("discritization: %d; episodes %d; max time per episode %d;" (precision_for_discretization, num_episodes, num_states_per_episode))

    state_count = {}

    state_action_count = {}

    Q = {}

    for i_episode in range(num_episodes):
        observation = env.reset()

        history = []

        final_reward = 0.0

        if i_episode % 100 == 0:
            print("starting: " + str(i_episode))

        for t in range(num_states_per_episode):
            # env.render()
            
            discretized_state = discretize(observation, precision_for_discretization)

            # determine some action to take...
            action = sample_action(discretized_state, state_count, Q, env.action_space)

            # Save what has happened...
            history.append(Decision(discretized_state, action))

            # Play out scene...
            observation, final_reward, done, info = env.step(action)

            if final_reward  >= 0:
                print("Success: episode %d; time %d" % (i_episode, t))
                env.render()

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break

        # Update all values...
        for decision in history:
            if decision.hash_state() not in state_count:
                    state_count[decision.hash_state()] = 0.0
        
            state_count[decision.hash_state()] += 1.0

            sa_hash = decision.hash_state_action()

            if sa_hash not in state_action_count:  
                state_action_count[sa_hash] = 0.0
                Q[sa_hash] = 0.0

            state_action_count[sa_hash] += 1.0
            Q[sa_hash] += (1.0 / state_action_count[sa_hash]) * (final_reward - Q[sa_hash]) 

                


if __name__ == "__main__":
    mc_main()