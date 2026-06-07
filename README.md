# Retail Inventory Replenishment using Q-Learning

## Project Overview

Inventory replenishment is a common problem in retail operations. Ordering too little inventory can lead to stockouts and lost sales, while ordering too much inventory increases holding costs and ties up capital.

The objective of this project is to train a reinforcement learning agent that learns how much inventory to order each day. The learned policy is compared against a simple rule-based replenishment strategy to determine whether reinforcement learning can improve operational performance.

## Business Problem

Imagine a small retailer that needs to decide how much inventory to reorder every day. Demand changes from day to day and future demand is uncertain. The retailer wants to maximize profit while keeping enough inventory available to satisfy customers.

This problem is naturally sequential because today's ordering decision affects inventory availability and costs in future periods.

## Environment Design

The simulator models a simplified retail inventory system. Inventory arrives after a fixed lead time, customer demand is generated randomly, and the retailer earns revenue from sales while incurring inventory-related costs.

The agent observes three pieces of information before making a decision:

* Current inventory level (low, medium, or high)
* Recent demand level
* Whether there is already an order in transit

At each decision point, the agent can choose one of four ordering quantities: 0, 10, 25, or 50 units.

The reward function is designed to encourage profitable behavior while discouraging stockouts and excessive inventory. Revenue from sales contributes positively to reward, while purchasing costs, holding costs, ordering costs, and stockout penalties reduce it.

## Baseline Policy

To provide a meaningful benchmark, a simple rule-based inventory policy was implemented.

The baseline follows a common business heuristic:

* Order 50 units when inventory is low
* Order 25 units when inventory is moderate
* Do not order when inventory is high

Although simple, this type of policy is frequently used in practice and provides a useful benchmark for evaluating the RL agent.

## Reinforcement Learning Approach

The learning agent uses tabular Q-Learning with epsilon-greedy exploration.

The agent interacts with the environment repeatedly over 3,000 training episodes and gradually learns action values for different inventory situations. Exploration is reduced over time so that the agent increasingly relies on learned experience rather than random actions.

## Results

The final evaluation compared the learned policy with the rule-based baseline.

| Policy     | Average Reward | Average Stockout Days |
| ---------- | -------------- | --------------------- |
| Baseline   | 6906.31        | 0.23                  |
| Q-Learning | 3871.65        | 33.73                 |

Contrary to expectations, the Q-Learning agent performed significantly worse than the baseline policy. The learned policy maintained very low inventory levels and experienced frequent stockouts, which greatly reduced overall profitability.

## Discussion

One of the most interesting findings from this project is that reinforcement learning did not automatically outperform a simple business rule.

The poor performance appears to be driven by limitations in the state representation and the simplified nature of the simulator. Important factors such as seasonality, demand trends, promotions, and supplier uncertainty were not included in the state space.

As a result, the agent often underestimated future inventory needs and allowed inventory levels to become critically low.

This outcome highlights an important lesson in reinforcement learning: algorithm choice is often less important than state design, reward design, and environment quality.

## Edge Case Analysis

In addition to comparing average performance, it is useful to consider how the policies behave under more challenging situations.

When demand spikes unexpectedly, the baseline policy tends to recover inventory levels quickly because it places large replenishment orders whenever inventory becomes low. The Q-learning agent, however, often reacts too slowly and experiences extended periods of stockouts.

When inventory levels start at very low values, the baseline policy again responds aggressively by replenishing inventory immediately. The learned policy frequently delays ordering decisions, which increases the risk of lost sales.

These observations suggest that the baseline policy is more robust under stressful operating conditions, while the RL agent remains sensitive to inventory shortages and demand variability.


## Risks and Limitations

Several risks were identified during the project.

First, the agent may learn behaviors that optimize the mathematical reward without aligning with broader business objectives. Second, the simulator does not fully capture real-world retail demand patterns. Finally, the learned policy may be overfitted to the simulated environment and may not generalize to actual operations.

These limitations make direct deployment risky.

## Failure Analysis

One of the most important lessons from this project is understanding why the RL agent performed poorly despite being trained for thousands of episodes.

### Reward Hacking

Although the agent was designed to maximize long-term reward, the reward function may not perfectly represent business objectives. The agent appeared to learn a strategy that kept inventory levels extremely low in order to avoid purchasing and holding costs. While this behavior may occasionally improve short-term rewards, it resulted in frequent stockouts and lost sales. This demonstrates how an agent can optimize the reward function without actually achieving the desired business outcome.

### Unsafe Behavior

The learned policy would be considered unsafe in a real retail environment. During evaluation, the agent experienced an average of more than 33 stockout days per episode, compared with almost zero stockouts for the baseline policy. Such behavior would likely reduce customer satisfaction, damage brand reputation, and result in lost revenue.

### Instability

Training results were highly variable across episodes. Even after thousands of training episodes, reward values fluctuated significantly rather than converging toward a stable policy. This suggests that the agent struggled to learn a consistent inventory strategy under the current state representation and environment design.

### Overfitting

The agent was trained entirely within a simplified simulator. As a result, there is a risk that the learned policy is overfitted to the specific demand patterns generated by the simulation. Even if performance were improved within the simulator, there would be no guarantee that the same policy would perform well under real-world demand conditions.

### Key Takeaway

The poor performance of the RL agent highlights an important challenge in reinforcement learning applications. Success depends not only on the learning algorithm itself, but also on the quality of the state representation, reward function, and simulation environment. In this project, these design choices had a larger impact on performance than the choice of Q-learning as the learning method.

## Recommendation

Based on the evaluation results, the current Q-Learning agent should not be deployed in production.

A more appropriate next step would be to run the model in shadow mode, where it generates recommendations while human managers continue making the final inventory decisions.

Future work should focus on improving the state representation, incorporating demand forecasting signals, and testing the agent under more realistic business conditions.
