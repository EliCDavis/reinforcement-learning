from util import *
import matplotlib.pyplot as plt


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


def best_policy_value(state, Q, num_actions):
    ha = state_with_action_hash(state, best_policy(state, Q, num_actions))

    if ha in Q:
        return Q[ha]

    return 0

def q_main(file_name, env, num_episodes, num_states_per_episode, discount_factor, precision_for_discretization):

    f= open( file_name + ".run","w+")
    f.write("strat: q; discritization: %d; episodes %d; max time per episode %d; discount factor: %f\n" % (precision_for_discretization, num_episodes, num_states_per_episode, discount_factor))
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
            # if i_episode > 900:
            #     env.render()
            
            # Play out scene...
            observation, reward, done, info = env.step(action)
            # nr = new_reward(observation)
            nr = reward
            # nr = -1.0
            # nr = reward if reward < 0 else 1

            discretized_state = discretize(observation, precision_for_discretization)

            inc_state_count(discretized_state, state_count)

            action_prime = sample_action(discretized_state, state_count, Q, env.action_space)

            inc_sa_count(discretized_state, action_prime, state_action_count, Q)

            sa_hash_prime = state_with_action_hash(discretized_state, action_prime)

            Q[sa_hash] += (1.0 / state_action_count[sa_hash]) * (nr + (best_policy_value(discretized_state, Q, env.action_space.n)*discount_factor) - Q[sa_hash]) 
            

            # Update values for next iteration...
            action = action_prime
            sa_hash = sa_hash_prime

            if done:
                # print("Episode finished after {} timesteps".format(t+1))
                # env.render()
                f.write("%d, %d\n" % (i_episode, t))
                x_axis.append(i_episode)
                y_axis.append(t)
                f.flush()
                break

    f.close()                
    plt.plot(x_axis, y_axis, 'ro')
    plt.title('Q - basic - Discount {:0.2f}'.format(discount_factor))
    plt.ylabel('Time To Win Episode')
    plt.xlabel('Number Episodes Trained')
    plt.savefig(file_name + ".png")
