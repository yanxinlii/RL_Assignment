import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.environment import InventoryEnvironment
from src.baseline_policy import BaselinePolicy
from src.q_learning_agent import QLearningAgent


def train_q_learning(episodes=3000):
    env = InventoryEnvironment()
    agent = QLearningAgent()
    reward_history = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)

            agent.update(state, action, reward, next_state)

            state = next_state
            total_reward += reward

        agent.decay_epsilon()
        reward_history.append(total_reward)

        if (episode + 1) % 500 == 0:
            print(f"Episode {episode + 1}: Reward = {total_reward:.2f}")

    return agent, reward_history


def evaluate_policy(policy_type, agent=None, episodes=200):
    env = InventoryEnvironment()
    rewards = []
    stockout_days = []
    average_inventory = []

    baseline = BaselinePolicy()

    if agent is not None:
        old_epsilon = agent.epsilon
        agent.epsilon = 0

    for _ in range(episodes):
        state = env.reset()
        total_reward = 0
        total_stockouts = 0
        inventory_levels = []
        done = False

        while not done:
            if policy_type == "baseline":
                action = baseline.choose_action(state)
            else:
                action = agent.choose_action(state)

            next_state, reward, done, info = env.step(action)

            total_reward += reward

            if info["lost_sales"] > 0:
                total_stockouts += 1

            inventory_levels.append(info["inventory"])
            state = next_state

        rewards.append(total_reward)
        stockout_days.append(total_stockouts)
        average_inventory.append(np.mean(inventory_levels))

    if agent is not None:
        agent.epsilon = old_epsilon

    return {
        "average_reward": np.mean(rewards),
        "worst_episode_reward": np.min(rewards),
        "average_stockout_days": np.mean(stockout_days),
        "average_inventory": np.mean(average_inventory),
    }


def make_plots(reward_history, results_df):
    plt.figure(figsize=(10, 6))
    plt.plot(reward_history)
    plt.title("Q-Learning Training Reward Curve")
    plt.xlabel("Episode")
    plt.ylabel("Total Episode Reward")
    plt.grid(True)
    plt.savefig("outputs/reward_curve.png")
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.bar(results_df["policy"], results_df["average_reward"])
    plt.title("Average Reward: Baseline vs Q-Learning")
    plt.xlabel("Policy")
    plt.ylabel("Average Reward")
    plt.grid(axis="y")
    plt.savefig("outputs/performance_comparison.png")
    plt.close()


def main():
    os.makedirs("outputs", exist_ok=True)

    print("Training Q-learning agent...")
    agent, reward_history = train_q_learning()

    pd.DataFrame({
        "episode": range(1, len(reward_history) + 1),
        "reward": reward_history
    }).to_csv("outputs/training_rewards.csv", index=False)

    print("\nEvaluating baseline...")
    baseline_results = evaluate_policy("baseline")

    print("Evaluating Q-learning agent...")
    q_learning_results = evaluate_policy("q_learning", agent=agent)

    results_df = pd.DataFrame([
        {
            "policy": "Baseline",
            **baseline_results
        },
        {
            "policy": "Q-Learning",
            **q_learning_results
        }
    ])

    results_df.to_csv("outputs/evaluation_results.csv", index=False)

    make_plots(reward_history, results_df)

    print("\nEvaluation Results:")
    print(results_df)

    print("\nSaved outputs:")
    print("outputs/training_rewards.csv")
    print("outputs/evaluation_results.csv")
    print("outputs/reward_curve.png")
    print("outputs/performance_comparison.png")


if __name__ == "__main__":
    main()