# src/env.py

import random
from typing import List

class Env:
    def __init__(
        self,
        agents: List,
        initial_p_green: float,
        initial_p_oil:   float,
        initial_pv_green: float,
        initial_pv_oil:   float,
        initial_fare:     float,
        initial_feebate_rate: float
    ):
        self.agents         = agents
        self.p_green        = initial_p_green
        self.p_oil          = initial_p_oil
        self.pv_green       = initial_pv_green
        self.pv_oil         = initial_pv_oil
        self.fare           = initial_fare
        self.feebate_rate   = initial_feebate_rate

        self.update_totals()
        self.demand = self.fare * (self.total_n_oil + self.total_n_green)

    def update_totals(self):
        self.total_n_oil   = sum(a.n_oil   for a in self.agents)
        self.total_n_green = sum(a.n_green for a in self.agents)
        self.total_n       = self.total_n_oil + self.total_n_green

    def market(self):
        self.p_oil  *= 1 + random.uniform(-0.10, 0.10)
        self.pv_oil *= 1 + random.uniform(-0.10, 0.10)

        self.p_green  = max(self.p_green, self.p_oil/2) * (1 + random.uniform(-0.10, 0))
        self.pv_green = (
            max(min(180, 180*200*4/(self.total_n_green+1)), 70)
            * (1 + random.uniform(-0.05, 0.05))
        )

    def feebate(self):
        sum_oil   = self.total_n_oil
        sum_green = self.total_n_green
        rate = self.feebate_rate

        penalty_rate = ((self.p_green - self.p_oil * rate) * sum_green / sum_oil) if sum_oil else 0
        rebate_rate  = (self.p_green - self.p_oil * rate) if sum_oil else 0

        penalty_rate = max(0, penalty_rate)
        rebate_rate  = max(0, rebate_rate)

        for a in self.agents:
            a.benefit -= penalty_rate * a.n_oil
            a.benefit += rebate_rate  * a.n_green

    def update(self):
        self.update_totals()
        # 需要は年2.5%増加
        self.fare   *= 1.025
        self.market()
        self.feebate()
        self.update_totals()
