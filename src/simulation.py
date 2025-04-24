# src/simulation.py

import random
from .agent import Agent
from .env import Env
from .utils import DISCOUNT_RATE

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
        # エージェント生成
        self.agents = [Agent(i) for i in range(N)]
        # 環境生成
        self.env = Env(
            self.agents,
            initial_p_green, initial_p_oil,
            initial_pv_green, initial_pv_oil,
            initial_fare, initial_feebate_rate
        )
        # 記録用リスト
        self.years = []
        # …その他ヒストリも初期化…

    def run(self):
        for year in range(2020, 2020 + self.time):
            self.years.append(year)
            for a in self.agents:
                a.trade(self.env, self.agents, year)
            self.env.update()
            for a in self.agents:
                a.renew(self.env, year)
            # …ヒストリに保存…
            print(f"Year {year}: total_oil={self.env.total_n_oil}, total_green={self.env.total_n_green}")

    def plot(self):
        # matplotlib で各種履歴をプロット
        pass

    def validate(self):
        # 2050年到達時点での検証
        pass

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    sim.plot()
    sim.validate()
