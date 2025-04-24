# src/simulation.py

import random
import matplotlib.pyplot as plt
from .agent import Agent
from .env import Env

class Simulation:
    def __init__(
        self,
        N: int = 4,
        time: int = 50,
        initial_p_green: float = 83.55,
        initial_p_oil:   float = 13.64,
        initial_pv_green: float = 180,
        initial_pv_oil:   float = 70,
        initial_fare:     float = 144.8,
        initial_feebate_rate: float = 0.1,
    ):
        random.seed(42)
        self.time = time

        # エージェント＆環境
        self.agents = [Agent(i) for i in range(N)]
        self.env    = Env(
            self.agents,
            initial_p_green, initial_p_oil,
            initial_pv_green, initial_pv_oil,
            initial_fare, initial_feebate_rate
        )

        # 記録用リスト
        self.years                 = []
        self.total_n_green_history = []
        self.total_n_oil_history   = []
        self.total_n_history       = []
        self.p_green_history       = []
        self.p_oil_history         = []
        self.pv_green_history      = []
        self.pv_oil_history        = []
        self.fare_history          = []
        self.demand_history        = []
        self.agent_avg_oil         = []
        self.agent_avg_green       = []
        self.feebate_rate_history  = []
        self.agent_benefit_history = [[] for _ in range(N)]

    def run(self):
        for year in range(2020, 2020 + self.time):
            self.years.append(year)

            # 各エージェント売買
            for a in self.agents:
                a.trade(self.env, self.agents, year)

            # 環境更新 → 各エージェント決算
            self.env.update()
            for a in self.agents:
                a.renew(self.env, year)

            # ヒストリに保存
            self.total_n_green_history.append(self.env.total_n_green)
            self.total_n_oil_history.append(self.env.total_n_oil)
            self.total_n_history.append(self.env.total_n)
            self.p_green_history.append(self.env.p_green)
            self.p_oil_history.append(self.env.p_oil)
            self.pv_green_history.append(self.env.pv_green)
            self.pv_oil_history.append(self.env.pv_oil)
            self.fare_history.append(self.env.fare)
            self.demand_history.append(self.env.demand)
            self.agent_avg_oil.append(
                sum(a.n_oil for a in self.agents)/len(self.agents)
            )
            self.agent_avg_green.append(
                sum(a.n_green for a in self.agents)/len(self.agents)
            )
            self.feebate_rate_history.append(self.env.feebate_rate)

            for idx, a in enumerate(self.agents):
                self.agent_benefit_history[idx].append(a.benefit)

            print(f"\rYear: {year}, Oil:{self.env.total_n_oil}, Green:{self.env.total_n_green}", end="")
        print()

    def plot(self):
        # 簡易テキスト出力
        print("Year\tTotal\tDemand\tFare")
        for y, tot, d, f in zip(self.years, self.total_n_history, self.demand_history, self.fare_history):
            print(f"{y}\t{tot}\t{d:.1f}\t{f:.1f}")

        # グラフ（適宜調整してください）
        plt.figure(figsize=(12, 8))
        plt.plot(self.years, self.total_n_oil_history,   label="Oil Ships")
        plt.plot(self.years, self.total_n_green_history, label="Green Ships")
        plt.legend()
        plt.title("Total Ships Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Ships")
        plt.tight_layout()
        plt.show()

    def validate(self):
        # 例: 2050年到達時点での検証
        if 2050 in self.years:
            idx = self.years.index(2050)
            oil_2050 = self.total_n_oil_history[idx]
            print("2050年 Oil Ships:", oil_2050)
        else:
            print("（2050年はシミュレーション期間外です）")

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    sim.plot()
    sim.validate()
