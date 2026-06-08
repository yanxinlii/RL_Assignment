import pandas as pd
import matplotlib.pyplot as plt


def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + (height * 0.02),
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )


df_rewards = pd.read_csv("outputs/training_rewards.csv")
df_eval = pd.read_csv("outputs/evaluation_results.csv")


# 1. Training reward curve
plt.figure(figsize=(10, 6))

plt.plot(df_rewards["episode"], df_rewards["reward"])

plt.title("Q-Learning Training Reward Curve")
plt.xlabel("Episode")
plt.ylabel("Total Episode Reward")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("outputs/reward_curve.png")
plt.close()


# 2. Average reward comparison
plt.figure(figsize=(8, 6))

bars = plt.bar(
    df_eval["policy"],
    df_eval["average_reward"]
)

plt.title("Average Reward by Policy")
plt.xlabel("Policy")
plt.ylabel("Average Reward")
plt.grid(axis="y", alpha=0.3)

add_value_labels(bars)

plt.tight_layout()
plt.savefig("outputs/performance_comparison.png")
plt.close()


# 3. Average stockout days comparison
plt.figure(figsize=(8, 6))

bars = plt.bar(
    df_eval["policy"],
    df_eval["average_stockout_days"]
)

plt.title("Average Stockout Days by Policy")
plt.xlabel("Policy")
plt.ylabel("Stockout Days per Episode")
plt.grid(axis="y", alpha=0.3)

add_value_labels(bars)

plt.tight_layout()
plt.savefig("outputs/stockout_comparison.png")
plt.close()


# 4. Average inventory comparison
plt.figure(figsize=(8, 6))

bars = plt.bar(
    df_eval["policy"],
    df_eval["average_inventory"]
)

plt.title("Average Inventory Level by Policy")
plt.xlabel("Policy")
plt.ylabel("Average Inventory Units")
plt.grid(axis="y", alpha=0.3)

add_value_labels(bars)

plt.tight_layout()
plt.savefig("outputs/inventory_comparison.png")
plt.close()


print("All plots saved successfully.")