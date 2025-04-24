# src/models/rd_no_feebate_model.py
import random
from ..agent import Agent as BaseAgent
from ..utils import DISCOUNT_RATE

class Agent(BaseAgent):
    def __init__(self,i):
        super().__init__(i)
        # グリーン船をほぼゼロスタートに
        self.n_green = random.randint(0,1)

    def trade(self, env, others, year):
        # フィーベイト計算をスキップ
        # → predict_feebate_future を呼ばない or 全部ゼロに
        super().trade(env, others, year)

# Env は base と同じので省略
Agent = Agent
from ..env import Env
