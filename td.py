from util import *
import matplotlib.pyplot as plt

# def new_reward(orentation):
#     return orentation[0] / -1

def inc_state_count(state, state_count):
    if str(state) not in state_count:
        state_count[str(state)] = 0.0

    state_count[str(state)] += 1.0

def inc_sa_count(state, action, state_action_count, Q):
    sa_hash = state_with_action_hash(state, action)

    if sa_hash not in state_action_count:  
        state_action_count[sa_hash] = 0.0
        Q[sa_hash] = 0.0

    state_action_count[sa_hash] += 1.0

def td_main(file_name, env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization):

    f= open( file_name + ".run","w+")
    f.write("strat: td; discritization: %d; episodes %d; max time per episode %d; discount factor: %f\n" % (precision_for_discretization, num_episodes, num_states_per_episode, discount_factor))
    f.write("episode, time\n")

    # graphing purposes
    x_axis = []
    y_axis = []

    state_count = {}
    state_action_count = {}
    Q = {}

    for i_episode in range(num_episodes):
        observation = env.reset()

        if i_episode % 100 == 0:
            print("starting: " + str(i_episode))

        discretized_state = discretize(observation, precision_for_discretization)
        inc_state_count(discretized_state, state_count)

        action = sample_action(discretized_state, state_count, Q, env.action_space)
        inc_sa_count(discretized_state, action, state_action_count, Q)

        sa_hash = state_with_action_hash(discretized_state, action)

        for t in range(num_states_per_episode):
            # env.render()
            
            # Play out scene...
            observation, reward, done, info = env.step(action)
            # nr = new_reward(observation)
            # nr = reward
            nr = reward if reward < 0 else 1

            discretized_state = discretize(observation, precision_for_discretization)

            inc_state_count(discretized_state, state_count)

            action_prime = sample_action(discretized_state, state_count, Q, env.action_space)

            inc_sa_count(discretized_state, action_prime, state_action_count, Q)

            sa_hash_prime = state_with_action_hash(discretized_state, action_prime)

            Q[sa_hash] += (1.0 / state_action_count[sa_hash]) * (nr + (Q[sa_hash_prime]*discount_factor) - Q[sa_hash]) 
            
            if reward  >= 0 :
                f.write("%d, %d\n" % (i_episode, t))
                x_axis.append(i_episode)
                y_axis.append(t)
                f.flush()
                # print(observation)
                # env.render()
                break

            # Update values for next iteration...
            action = action_prime
            sa_hash = sa_hash_prime

            # if done:
            #     print("Episode finished after {} timesteps".format(t+1))
            #     # env.render()
            #     break

    f.close()                
    plt.plot(x_axis, y_axis, 'ro')
    plt.title('TD - -1/1 - Discount {:0.2f}'.format(discount_factor))
    plt.ylabel('Time To Win Episode')
    plt.xlabel('Number Episodes Trained')
    plt.savefig(file_name + ".png")
