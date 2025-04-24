# src/models/rd_model.py
import random, numpy as np
from ..agent import Agent as BaseAgent
from ..env   import Env   as BaseEnv
from ..utils import MAX_REDUCTION_FACTOR

class Agent(BaseAgent):
    def __init__(self, i):
        super().__init__(i)
        self.investment_cutoff = 2050
        self.investment_type = random.choice(['Type1','Type2','Type3'])
        self.investment_rate = {'Type1':0.20,'Type2':0.10,'Type3':0.01}[self.investment_type]
        self.green_available_year = {'Type1':2026,'Type2':2028,'Type3':2030}[self.investment_type]

    def trade(self, env, others, year):
        # 研究投資
        if year < self.investment_cutoff:
            env.research_fund += self.benefit * self.investment_rate
        # 通常 trade 処理
        super().trade(env, others, year)

class Env(BaseEnv):
    def __init__(self, agents, p_g, p_o, pv_g, pv_o, fare, feebate_rate):
        self.research_fund = 0.0
        super().__init__(agents, p_g, p_o, pv_g, pv_o, fare, feebate_rate)

    def apply_research_effects(self):
        factor = max(MAX_REDUCTION_FACTOR, 1 - self.research_fund/1e8)
        self.pv_green *= factor
        self.p_green   *= factor

    def update(self):
        self.apply_research_effects()
        super().update()
