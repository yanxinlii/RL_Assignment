# Retail Inventory Replenishment using Q-Learning

## Project Overview

Inventory replenishment is a common operational challenge in retail businesses. Ordering too little inventory can result in stockouts and lost sales, while ordering too much inventory increases holding costs and ties up capital.

The objective of this project is to train a reinforcement learning agent that learns how much inventory to order each day. The learned policy is compared against a simple rule-based replenishment strategy to determine whether reinforcement learning can improve business performance.

Rather than focusing on model complexity, this project focuses on problem formulation, reward design, evaluation, and understanding the risks of deploying reinforcement learning in a business setting.

---

## Business Problem

Imagine a small retailer that must decide how much inventory to reorder every day.

Customer demand changes from day to day and future demand is uncertain. The retailer wants to maximize profit while ensuring products remain available for customers.

This is a sequential decision-making problem because today's ordering decision affects future inventory levels, future costs, and future sales opportunities.

---

# MDP Formulation

## State

The agent observes three pieces of information before making a decision:

- Current inventory level (low, medium, or high)
- Recent demand level
- Whether there is already an order in transit

The state representation is intentionally simple to allow the use of tabular Q-learning.

---

## Actions

At each decision point, the agent can choose one of four ordering quantities:

| Action | Order Quantity |
|----------|----------|
| 0 | 0 units |
| 1 | 10 units |
| 2 | 25 units |
| 3 | 50 units |

---

## Reward Function

The reward function is designed to balance profitability and operational efficiency.

Positive reward:

- Revenue generated from sales

Negative reward:

- Inventory purchasing costs
- Inventory holding costs
- Ordering costs
- Stockout penalties

The goal is to encourage the agent to maintain enough inventory to satisfy demand while avoiding excessive inventory costs.

---

## Transition Dynamics

Each simulated day follows the process below:

1. Existing inventory orders may arrive.
2. Customer demand is generated.
3. Sales occur based on available inventory.
4. Lost sales are recorded if demand exceeds inventory.
5. Inventory levels are updated.
6. The agent chooses a replenishment action.
7. The environment transitions to the next state.

---

## Horizon

- One episode represents 60 business days.
- The agent is trained for 3,000 episodes.
- Final evaluation is performed over 200 episodes.

---

# Baseline Policy

To provide a meaningful benchmark, a simple rule-based inventory policy was implemented.

The baseline follows a common business heuristic:

- Order 50 units when inventory is low
- Order 25 units when inventory is moderate
- Do not order when inventory is high

Although simple, this policy reflects the type of replenishment rule often used in practice and serves as a useful benchmark for evaluating the RL agent.

---

# Reinforcement Learning Approach

The learning agent uses tabular Q-Learning with epsilon-greedy exploration.

Training settings:

- Learning rate (α): 0.1
- Discount factor (γ): 0.95
- Initial epsilon: 1.0
- Minimum epsilon: 0.05
- Epsilon decay: 0.995

The agent interacts with the environment repeatedly and gradually learns which actions generate the highest long-term reward in different inventory situations.

---

# Evaluation Results

The final evaluation compared the learned policy with the rule-based baseline.

| Policy | Average Reward | Average Stockout Days | Average Inventory |
|----------|----------|----------|----------|
| Baseline | 6906.31 | 0.23 | 46.65 |
| Q-Learning | 3871.65 | 33.73 | 2.69 |

Contrary to expectations, the Q-Learning agent performed significantly worse than the baseline policy.

While the RL agent successfully learned a policy from experience, it consistently maintained very low inventory levels, which led to frequent stockouts and reduced profitability.

---

# Generated Outputs

The project automatically generates the following files:

- outputs/training_rewards.csv
- outputs/evaluation_results.csv
- outputs/reward_curve.png
- outputs/performance_comparison.png
- outputs/inventory_comparison.png
- outputs/stockout_comparison.png

---

# Policy Behavior Analysis

The visualizations provide insight into why the Q-learning agent underperformed.

The training reward curve shows that the agent never converged to a clearly stable policy. Although rewards improved during some portions of training, performance remained highly variable throughout the 3,000 episodes.

The average reward comparison confirms that the baseline policy generated substantially higher rewards than the learned policy.

The inventory comparison reveals an important behavioral difference. The baseline policy maintained an average inventory level of approximately 46.65 units, while the Q-learning agent maintained only 2.69 units on average. This suggests that the learned policy became overly focused on reducing inventory costs.

The stockout comparison explains the poor financial performance of the RL agent. By keeping inventory levels too low, the agent experienced an average of 33.73 stockout days per episode, compared with only 0.23 stockout days for the baseline policy.

Taken together, the results suggest that the learned policy developed an overly aggressive inventory reduction strategy. While inventory costs decreased, service levels deteriorated significantly, leading to lower overall profitability.

---

# Discussion

One of the most interesting findings from this project is that reinforcement learning did not automatically outperform a simple business rule.

The poor performance appears to be driven by limitations in the state representation and the simplified nature of the simulator. Important factors such as seasonality, demand trends, supplier reliability, promotions, and external market conditions were not included in the state space.

As a result, the agent often underestimated future inventory needs and allowed inventory levels to become critically low.

This outcome highlights an important lesson in reinforcement learning: the quality of the state representation, reward function, and environment design can be more important than the learning algorithm itself.

---

# Edge Case Analysis

In addition to comparing average performance, it is useful to consider how the policies behave under more challenging situations.

When demand spikes unexpectedly, the baseline policy tends to recover inventory levels quickly because it places large replenishment orders whenever inventory becomes low.

The Q-learning agent, however, often reacts too slowly and experiences extended periods of stockouts.

Similarly, when inventory starts at very low levels, the baseline policy replenishes aggressively, while the learned policy frequently delays ordering decisions.

These observations suggest that the baseline policy is more robust under stressful operating conditions, whereas the RL agent remains sensitive to inventory shortages and demand variability.

---

# Failure Analysis

One of the most important lessons from this project is understanding why the RL agent performed poorly despite being trained for thousands of episodes.

## Reward Hacking

The agent appeared to learn a strategy that minimized inventory and holding costs. While this occasionally improved short-term rewards, it resulted in frequent stockouts and lost sales.

This demonstrates how an RL agent can optimize the mathematical reward function without achieving the desired business outcome.

## Unsafe Behavior

The learned policy would be considered unsafe in a real retail environment.

An average of more than 33 stockout days per episode would lead to poor customer experience, reduced revenue, and potential reputational damage.

## Instability

Training rewards remained highly variable throughout training.

The reward curve suggests that the agent struggled to converge to a stable replenishment strategy under the current state representation.

## Overfitting

The agent was trained entirely within a simplified simulation environment.

Even if performance improved inside the simulator, there is no guarantee that the learned policy would generalize to real-world retail demand patterns.

## Governance Risk

Automated inventory decisions directly affect revenue and customer satisfaction.

Without appropriate monitoring and human oversight, a poorly behaving RL policy could create significant operational and financial risk.

---

# Recommendation

Based on the evaluation results, the current Q-Learning agent should not be deployed directly into production.

A more appropriate next step would be to run the model in shadow mode, where it generates replenishment recommendations while inventory managers continue making the final decisions.

Future work should focus on:

- Improving the state representation
- Incorporating demand forecasting information
- Redesigning the reward function
- Testing more realistic demand scenarios
- Comparing against stronger RL approaches such as DQN or PPO

Overall, this project demonstrates the reinforcement learning workflow successfully, but the current policy is not yet strong enough to replace a simple inventory management rule. Additional development and validation would be required before considering real-world deployment.