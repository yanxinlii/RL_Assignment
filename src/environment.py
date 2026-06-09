import numpy as np


class InventoryEnvironment:
    def __init__(self):

        self.max_inventory = 100

        self.lead_time = 2

        self.selling_price = 20

        self.unit_cost = 10

        self.holding_cost = 0.2

        self.stockout_penalty = 25

        self.order_cost = 20

        self.episode_length = 60

        self.actions = [0, 10, 25, 50]

        self.reset()

    def reset(self):

        self.day = 0

        self.inventory = 50

        self.pending_orders = []

        self.current_demand_level = 1

        return self._get_state()

    def _get_state(self):

        if self.inventory < 10:
            inventory_bucket = 0
        elif self.inventory < 25:
            inventory_bucket = 1
        elif self.inventory < 50:
            inventory_bucket = 2
        elif self.inventory < 75:
            inventory_bucket = 3
        else:
            inventory_bucket = 4

        demand_bucket = self.current_demand_level

        pending_bucket = 0 if len(self.pending_orders) == 0 else 1

        return (
            inventory_bucket,
            demand_bucket,
            pending_bucket
        )

    def generate_demand(self):

        demand_level = np.random.choice(
            [0, 1, 2],
            p=[0.3, 0.5, 0.2]
        )

        if demand_level == 0:
            demand = np.random.randint(5, 11)

        elif demand_level == 1:
            demand = np.random.randint(10, 21)

        else:
            demand = np.random.randint(20, 36)

        return demand, demand_level

    def step(self, action_index):

        order_quantity = self.actions[action_index]

        if order_quantity > 0:
            self.pending_orders.append(
                [self.lead_time, order_quantity]
            )

        arrived_inventory = 0

        updated_orders = []

        for days_left, qty in self.pending_orders:

            days_left -= 1

            if days_left <= 0:
                arrived_inventory += qty
            else:
                updated_orders.append(
                    [days_left, qty]
                )

        self.pending_orders = updated_orders

        self.inventory += arrived_inventory

        self.inventory = min(
            self.inventory,
            self.max_inventory
        )

        demand, demand_level = self.generate_demand()

        self.current_demand_level = demand_level

        sales = min(
            self.inventory,
            demand
        )

        lost_sales = max(
            0,
            demand - sales
        )

        self.inventory -= sales

        revenue = sales * self.selling_price

        purchase_cost = arrived_inventory * self.unit_cost

        holding_cost = (
            self.inventory *
            self.holding_cost
        )

        stockout_cost = (
            lost_sales *
            self.stockout_penalty
        )

        fixed_order_cost = (
            self.order_cost
            if order_quantity > 0
            else 0
        )

        reward = (
            revenue
            - purchase_cost
            - holding_cost
            - stockout_cost
            - fixed_order_cost
        )

        self.day += 1

        done = (
            self.day >=
            self.episode_length
        )

        next_state = self._get_state()

        info = {
            "sales": sales,
            "lost_sales": lost_sales,
            "inventory": self.inventory
        }

        return (
            next_state,
            reward,
            done,
            info
        )