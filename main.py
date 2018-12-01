from util import *
import datetime
from decision import Decision
import gym
import matplotlib.pyplot as plt

env = gym.make('Acrobot-v1')

precision_for_discretization = 2

num_episodes = 10000

num_states_per_episode = 499

discount_factor = 0.95

def mc_main():

    file_name = "runs/" + datetime.datetime.now().strftime("%Y-%m-%d %H %M")

    f= open( file_name + ".run","w+")
    f.write("discritization: %d; episodes %d; max time per episode %d; discount factor: %f\n" % (precision_for_discretization, num_episodes, num_states_per_episode, discount_factor))
    f.write("episode, time\n")
    state_count = {}

    x_axis = []
    y_axis = []

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
                final_reward = 1
                f.write("%d, %d\n" % (i_episode, t))
                x_axis.append(i_episode)
                y_axis.append(t)
                f.flush()
                # env.render()
                break

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break

        # Update all values...
        d_i = 0
        for decision in history:
            d_i += 1
            if decision.hash_state() not in state_count:
                    state_count[decision.hash_state()] = 0.0
        
            state_count[decision.hash_state()] += 1.0

            sa_hash = decision.hash_state_action()

            if sa_hash not in state_action_count:  
                state_action_count[sa_hash] = 0.0
                Q[sa_hash] = 0.0

            state_action_count[sa_hash] += 1.0
            Q[sa_hash] += (1.0 / state_action_count[sa_hash]) * ((final_reward * pow(discount_factor, len(history))) - Q[sa_hash]) 

    f.close()                
    plt.plot(x_axis, y_axis, 'ro')
    plt.title('Monte Carlo - Basic Reward')
    plt.ylabel('Time To Win Episode')
    plt.xlabel('Number Episodes Trained')
    plt.savefig(file_name + ".png")


if __name__ == "__main__":
    mc_main()