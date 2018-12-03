from util import *
from decision import Decision
import matplotlib.pyplot as plt

# def new_reward(orentation):
#     return orentation[0] / -1

def mc_main(file_name, env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization):

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
            observation, reward, done, info = env.step(action)

            final_reward += reward * pow(discount_factor, t)
            if reward  >= 0 :
                f.write("%d, %d\n" % (i_episode, t))
                x_axis.append(i_episode)
                y_axis.append(t)
                f.flush()
                break

            # if done:
            #     print("Episode finished after {} timesteps".format(t+1))
            #     # env.render()
            #     break

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
            Q[sa_hash] += (1.0 / state_action_count[sa_hash]) * (final_reward - Q[sa_hash]) 

    f.close()                
    plt.plot(x_axis, y_axis, 'ro')
    plt.title('Monte Carlo - Custom Reward - Discount {:0.2f}'.format(discount_factor))
    plt.ylabel('Time To Win Episode')
    plt.xlabel('Number Episodes Trained')
    plt.savefig(file_name + ".png")
