class BaselinePolicy:

    def choose_action(self, state):

        inventory_bucket = state[0]

        if inventory_bucket == 0:
            return 3

        elif inventory_bucket == 1:
            return 2

        else:
            return 0