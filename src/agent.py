# src/agent.py

import random
from typing import List, Tuple
import numpy as np
from .utils import DISCOUNT_RATE
from .prediction import predict_n_future, predict_feebate_future

class Agent:
    def __init__(self, i: int):
        self.ind       = i
        self.n_green   = random.randint(0, 5)
        self.n_oil     = random.randint(150, 250)
        self.benefit   = 0.0
        self.last_benefit = 0.0

        # ログ
        self.history_oil             = []
        self.history_green           = []
        self.history_predict_n_oil   = []
        self.history_predict_n_green = []

    def renew(self, env, year: int):
        """
        年次決算：コスト・売上から利益計算
        """
        cost = (
            self.n_oil   * (env.pv_oil   / 20 + env.p_oil)
          + self.n_green * (env.pv_green / 20 + env.p_green)
        )
        revenue = (self.n_oil + self.n_green) * env.fare
        self.last_benefit = self.benefit
        self.benefit      = revenue - cost

    def trade(self, env, other_agents: List["Agent"], year: int):
        """
        売買最適化：予測→試行→最大NPVを取る船数を決定
        """
        n_oil_old   = self.n_oil
        n_green_old = self.n_green

        past_years   = random.randint(3, 7)
        future_years = random.randint(1, 3)

        pred_oils, pred_greens = predict_n_future(self, env, other_agents, past_years, future_years)

        max_benefit = -1e9
        best_doil   = 0
        best_dgreen = 0
        best_pred_oils   = pred_oils
        best_pred_greens = pred_greens

        test_case = 500
        for d_oil in range(-test_case, test_case+1, 10):
            for d_green in range(-test_case, test_case+1, 10):
                n_oil   = max(0, self.n_oil   + d_oil)
                n_green = max(0, self.n_green + d_green)

                tot_oils   = pred_oils   + n_oil
                tot_greens = pred_greens + n_green

                penalties, rebates = predict_feebate_future(
                    self, env, tot_oils, tot_greens,
                    n_oil, n_green, future_years
                )

                npv = 0.0
                for i in range(future_years):
                    cost_i = (
                        (n_oil   + d_oil   * i) * (env.pv_oil   / 20 + env.p_oil)
                      + (n_green + d_green * i) * (env.pv_green / 20 + env.p_green)
                    )
                    denom = tot_oils[i] + tot_greens[i]
                    fare_i = env.fare * 1.025 ** (i+1) * env.total_n / denom if denom else 0
                    sales_i = (n_oil + d_oil*i + n_green + d_green*i) * fare_i

                    npv += (sales_i - cost_i - penalties[i] + rebates[i]) * (1 - DISCOUNT_RATE) ** (i+1)

                if npv > max_benefit:
                    max_benefit      = npv
                    best_doil        = d_oil
                    best_dgreen      = d_green
                    best_pred_oils   = tot_oils
                    best_pred_greens = tot_greens

        # 決定 → 更新
        self.history_predict_n_oil.append(best_pred_oils)
        self.history_predict_n_green.append(best_pred_greens)

        self.n_oil   = max(0, self.n_oil   + best_doil)
        self.n_green = max(0, self.n_green + best_dgreen)

        self.history_oil.append(self.n_oil   - n_oil_old)
        self.history_green.append(self.n_green - n_green_old)
