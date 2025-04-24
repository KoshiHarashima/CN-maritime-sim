# src/models/decreasing_feebate_model.py
import numpy as np
from ..prediction import predict_n_future, predict_feebate
from ..agent      import Agent as BaseAgent
from ..env        import Env   as BaseEnv

class Agent(BaseAgent):
    def predict_feebate_future(self, env, n_oils, n_greens, so, sg, fy):
        penalties = np.zeros(fy); rebates = np.zeros(fy)
        for i in range(fy):
            rate = env.feebate_rate * (1 - env.feebate_change_rate)**(i+1)
            p, r = predict_feebate(self, env, n_oils[i], n_greens[i], so, sg, rate)
            penalties[i], rebates[i] = p, r
        return penalties, rebates

class Env(BaseEnv):
    def __init__(self, agents, p_g, p_o, pv_g, pv_o, fare, feebate_rate, feebate_change_rate=0.05):
        super().__init__(agents, p_g, p_o, pv_g, pv_o, fare, feebate_rate)
        self.feebate_change_rate = feebate_change_rate

    def update(self):
        super().update()
        # フィーベイト率の減少は prediction 内で使われるのでここは何もしなくても可
        # もし env.feebate_rate 自体も下げたいならここで更新
        self.feebate_rate *= (1 - self.feebate_change_rate)
