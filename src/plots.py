import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "outputs/training_rewards.csv"
)

plt.figure(figsize=(10,6))

plt.plot(df["reward"])

plt.title(
    "Q-Learning Training Rewards"
)

plt.xlabel("Episode")

plt.ylabel("Reward")

plt.grid(True)

plt.savefig(
    "outputs/reward_curve.png"
)

plt.show()