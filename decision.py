
class Decision:

    def __init__(self, state, action):
        self.__state = state
        self.__action = action

    def hash_state_action(self):
        return self.hash_state() + " - " + str(self.__action) 

    def hash_state(self):
        return str(self.__state)
