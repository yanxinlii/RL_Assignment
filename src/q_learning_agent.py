import numpy as np
from collections import defaultdict


class QLearningAgent:

    def __init__(
        self,
        alpha=0.1,
        gamma=0.95,
        epsilon=1.0,
        epsilon_decay=0.998,
        epsilon_min=0.05
    ):

        self.alpha = alpha
        self.gamma = gamma

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.q_table = defaultdict(
            lambda: np.zeros(4)
        )

    def choose_action(self, state):

        if np.random.random() < self.epsilon:

            return np.random.randint(4)

        return np.argmax(
            self.q_table[state]
        )

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        current_q = self.q_table[state][action]

        max_future_q = np.max(
            self.q_table[next_state]
        )

        new_q = current_q + self.alpha * (
            reward
            + self.gamma * max_future_q
            - current_q
        )

        self.q_table[state][action] = new_q

    def decay_epsilon(self):

        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )