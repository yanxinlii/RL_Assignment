# Retail Inventory Replenishment using Q-Learning

## Project Overview

Inventory replenishment is a common challenge in retail operations. Ordering too little inventory can lead to stockouts and lost sales, while ordering too much inventory increases holding costs and ties up capital that could be used elsewhere.

The objective of this project is to train a reinforcement learning agent that learns how much inventory to order each day. The performance of the learned policy is compared against a simple rule-based inventory policy to determine whether reinforcement learning can improve decision-making in a retail environment.

The focus of this project is not on building a complex model, but rather on properly defining the decision problem, designing a meaningful reward function, evaluating performance, and understanding the risks associated with deploying reinforcement learning systems in business settings.

---

## Business Problem

Consider a small retailer that needs to decide how much inventory to reorder every day.

Customer demand changes from day to day and future demand is uncertain. The retailer wants to maximize long-term profitability while ensuring products remain available for customers.

This is a sequential decision-making problem because today's inventory decisions affect future inventory levels, future sales opportunities, and future operating costs.

---

## MDP Formulation

### State

The agent observes the following information before making a decision:

* Current inventory level
* Recent demand level
* Whether there is already an order in transit

The state representation is intentionally simplified to make tabular Q-learning feasible while still capturing the key factors that influence inventory decisions.

### Actions

At each decision point, the agent can choose one of four ordering quantities:

| Action | Order Quantity |
| ------ | -------------- |
| 0      | 0 units        |
| 1      | 10 units       |
| 2      | 25 units       |
| 3      | 50 units       |

### Reward Function

The reward function combines several business objectives.

Positive reward:

* Revenue generated from product sales

Negative reward:

* Inventory purchasing costs
* Inventory holding costs
* Ordering costs
* Stockout penalties

The goal is to encourage profitable behavior while discouraging excessive inventory and frequent stockouts.

### Transition Dynamics

Each simulated day follows the same process:

1. Existing orders may arrive.
2. Customer demand is generated.
3. Sales occur based on available inventory.
4. Inventory levels are updated.
5. Lost sales are recorded when demand exceeds inventory.
6. The agent chooses a replenishment action.
7. The environment transitions to the next state.

### Horizon

* One episode represents 60 business days.
* The agent is trained for 3,000 episodes.
* Final evaluation is performed over 200 episodes.

---

## Baseline Policy

To provide a meaningful benchmark, a simple rule-based inventory policy was implemented.

The policy follows a common business heuristic:

* Order 50 units when inventory is low
* Order 25 units when inventory is moderate
* Do not order when inventory is high

Although simple, this type of replenishment strategy is frequently used in practice and serves as a useful baseline for evaluating the reinforcement learning agent.

---

## Reinforcement Learning Approach

The learning agent uses tabular Q-learning with epsilon-greedy exploration.

Training parameters:

* Learning rate (α): 0.1
* Discount factor (γ): 0.95
* Initial epsilon: 1.0
* Minimum epsilon: 0.05
* Epsilon decay: 0.998

The agent repeatedly interacts with the environment and gradually learns which actions produce the highest long-term rewards under different inventory conditions.

---

## Evaluation Results

The final evaluation compared the learned policy with the rule-based baseline.

| Policy     | Average Reward | Average Stockout Days | Average Inventory |
| ---------- | -------------- | --------------------- | ----------------- |
| Baseline   | 6993.89        | 4.71                  | 32.41             |
| Q-Learning | 7514.11        | 3.39                  | 28.22             |

The Q-learning agent outperformed the baseline policy across all key evaluation metrics.

The learned policy generated higher average rewards, experienced fewer stockout days, and maintained lower inventory levels. These results suggest that the agent was able to learn a more efficient balance between inventory availability and inventory carrying costs.

---

## Generated Outputs

The project automatically generates the following outputs:

* outputs/training_rewards.csv
* outputs/evaluation_results.csv
* outputs/reward_curve.png
* outputs/performance_comparison.png
* outputs/inventory_comparison.png
* outputs/stockout_comparison.png

---

## Policy Behavior Analysis

The visualizations provide useful insight into how the learned policy behaves.

The reward comparison shows that the Q-learning agent consistently achieved higher average rewards than the baseline policy. Although the improvement is not dramatic, it demonstrates that the agent was able to learn a competitive replenishment strategy through experience.

The inventory comparison reveals that the RL agent maintained lower average inventory levels than the baseline policy. This indicates that the learned strategy avoided carrying unnecessary inventory while still maintaining product availability.

The stockout comparison provides additional evidence that the learned policy is effective. Despite maintaining lower inventory levels, the Q-learning agent experienced fewer stockout days than the baseline policy.

Taken together, these results suggest that the learned policy found a better trade-off between inventory costs and service levels.

---

## Discussion

One of the most interesting findings from this project is that a relatively simple Q-learning agent was able to outperform a rule-based inventory policy.

This result suggests that reinforcement learning can discover inventory management strategies that are difficult to capture through fixed business rules. Rather than applying the same logic in every situation, the agent learned to adapt its ordering decisions based on the current state of the environment.

At the same time, the performance improvement should be interpreted carefully. The simulation environment used in this project is intentionally simplified and does not capture many factors that influence real-world inventory decisions, including seasonality, promotions, supplier disruptions, and changing customer preferences.

As a result, success in the simulation does not necessarily guarantee success in production.

---

## Edge Case Analysis

In addition to comparing average performance, it is useful to consider how the policies behave under more challenging situations.

When demand increases unexpectedly, the baseline policy responds using fixed ordering rules. While this often works reasonably well, it may either overreact or underreact depending on the situation.

The Q-learning agent, on the other hand, adapts its decisions based on the current state and learned experience. During testing, the learned policy generally maintained sufficient inventory while avoiding excessive stock accumulation.

These observations suggest that the learned policy is more flexible than the rule-based baseline and may be better equipped to handle variability in demand.

---

## Failure Analysis

Although the final results are encouraging, several risks remain.

### Reward Hacking

Reinforcement learning agents optimize the reward function provided to them, not necessarily the true business objective.

If the reward function is poorly designed, an agent may learn behaviors that maximize reward while creating undesirable operational outcomes.

### Instability

Training performance fluctuated significantly across episodes.

While the final policy performed well, reinforcement learning can sometimes produce unstable results depending on the environment and hyperparameter settings.

### Overfitting

The agent was trained entirely within a simulated environment.

There is a risk that the learned policy has adapted too closely to the specific demand patterns generated by the simulator and may not perform equally well under real-world conditions.

### Governance Risk

Inventory decisions directly affect customer satisfaction and financial performance.

Any automated decision-making system should include monitoring, performance reporting, and human oversight to ensure that unexpected behaviors can be identified and corrected quickly.

---

## Recommendation

Based on the evaluation results, the Q-learning agent demonstrates promising performance and outperformed the baseline policy in the simulated environment.

However, I would not recommend immediate deployment. The simulation environment is intentionally simplified and does not capture many real-world challenges faced by retail businesses.

A more appropriate next step would be to operate the model in shadow mode, where the agent generates recommendations while managers continue making the final inventory decisions. This would allow additional testing and validation without introducing operational risk.

Future work could focus on:

* Expanding the state representation
* Incorporating demand forecasting information
* Testing under more realistic demand conditions
* Comparing performance against more advanced RL approaches such as DQN or PPO

Overall, the project demonstrates that reinforcement learning can improve inventory replenishment decisions in a controlled environment. While additional validation is required, the results suggest that the approach has potential for practical business applications.
