import numpy as np

from environment import InventoryEnvironment
from baseline_policy import BaselinePolicy


def evaluate_baseline(episodes=200):
    env = InventoryEnvironment()
    policy = BaselinePolicy()

    rewards = []
    stockout_days = []
    avg_inventory = []

    for _ in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        total_stockouts = 0
        inventories = []

        while not done:
            action = policy.choose_action(state)
            next_state, reward, done, info = env.step(action)

            total_reward += reward

            if info["lost_sales"] > 0:
                total_stockouts += 1

            inventories.append(info["inventory"])
            state = next_state

        rewards.append(total_reward)
        stockout_days.append(total_stockouts)
        avg_inventory.append(np.mean(inventories))

    return {
        "average_reward": np.mean(rewards),
        "average_stockout_days": np.mean(stockout_days),
        "average_inventory": np.mean(avg_inventory),
    }