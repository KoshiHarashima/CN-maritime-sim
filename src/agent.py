# src/agent.py

import random
from typing import List, Tuple
import numpy as np

from .utils import DISCOUNT_RATE
from .prediction import predict_n_future, predict_feebate_future

class Agent:
    def __init__(self, i: int):
        self.ind = i
        self.n_green = random.randint(0, 5)
        self.n_oil   = random.randint(150, 250)
        self.benefit = 0.0
        self.history_oil = []
        self.history_green = []
        # (必要であれば) 予測ログもここで初期化

    def trade(self, env, other_agents: List["Agent"], year: int):
        """
        売買ロジックの雛形
        """
        # 1) 他エージェントの行動予測
        past_years   = random.randint(1, 3)
        future_years = random.randint(1, 5)
        predict_oils, predict_greens = predict_n_future(self, env, other_agents, past_years, future_years)

        # 2) 最適化ループ（例: 費用対効果最大化）
        #    → predict_feebate_future を呼び出してペナルティ・リベートを取得
        best_diff_oil, best_diff_green = 0, 0
        # …（既存ロジックをコピー＆調整ください）…

        # 3) 決定して数量更新
        self.n_oil   = max(0, self.n_oil   + best_diff_oil)
        self.n_green = max(0, self.n_green + best_diff_green)
        self.history_oil.append(self.n_oil)
        self.history_green.append(self.n_green)

    def renew(self, env, year: int):
        """
        年次決算処理。利益を計算して self.benefit を更新。
        """
        cost  = self.n_oil   * (env.pv_oil   / 20 + env.p_oil)
        cost += self.n_green * (env.pv_green / 20 + env.p_green)
        revenue = (self.n_oil + self.n_green) * env.fare

        self.benefit = revenue - cost
