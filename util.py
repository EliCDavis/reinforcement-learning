import random

def state_with_action_hash(state, action):
    return str(state) + " - " + str(action) 

def best_policy(state, Q, num_actions):
    best = -1
    best_value = -1000000
    for action in range(num_actions):
        ha = state_with_action_hash(state, action)
        if ha in Q and Q[ha] > best_value:
            best_value = Q[ha]
            best = action

    return best if best > -1 else random.randint(0, num_actions-1)

def sample_action(state, state_count, Q, action_space):
    """
    Determines an action to take given state and past obseravations
    
    returns index of actions to take
    """
    num_actions = action_space.n 

    n0 = 100.0 

    epsilon = 0
    if str(state) in state_count:
        epsilon = n0 / (n0 + state_count[str(state)])
    greedy_chance = (epsilon / num_actions) + 1.0 - epsilon
    best_action = best_policy(state, Q, num_actions)

    if random.random() < greedy_chance:
        return best_action
    else:
        canidates = list(range(num_actions))
        del canidates[best_action]
        return random.choice(canidates)

def discretize(state, decimalPlace):
    discritized_state = [None]*len(state)

    for state_index in range(len(state)):
        if state[state_index].is_integer():
            discritized_state[state_index] = state[state_index]
        else:
            discritized_state[state_index] = int(round(state[state_index] * pow(10, decimalPlace)))
    
    return discritized_state