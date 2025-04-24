# src/models/rd_transition_model.py
import random, numpy as np
from ..agent import Agent as BaseAgent
from ..env   import Env   as BaseEnv
from ..utils import MAX_REDUCTION_FACTOR

class Agent(BaseAgent):
    def __init__(self,i):
        super().__init__(i)
        self.start_year = 2020
        self.investment_type = random.choice(['Type1','Type2','Type3'])
        self._upd_props()

    def _upd_props(self):
        self.investment_rate       = {'Type1':0.20,'Type2':0.10,'Type3':0.01}[self.investment_type]
        self.green_available_year  = {'Type1':2026,'Type2':2028,'Type3':2030}[self.investment_type]

    def trade(self, env, others, year):
        # タイプアップグレード
        elapsed = year - self.start_year
        if self.investment_type=='Type3' and elapsed>=15:
            self.investment_type='Type2'; self._upd_props()
        if self.investment_type=='Type2' and elapsed>=25:
            self.investment_type='Type1'; self._upd_props()

        super().trade(env, others, year)

class Env(BaseEnv):
    # R&D モデルと同じ実装
    #  (rd_model.py の Env をコピペ)
    pass
