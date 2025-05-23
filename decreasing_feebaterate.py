import linear_pred
import base
import numpy as np


class CustomAgent(linear_pred.CustomAgent):
    def predict_feebate_future(self, env, n_oils :np.ndarray, n_greens :np.ndarray, self_n_oil, self_n_green, future_years):
        penalties = np.zeros(future_years)
        rebates = np.zeros(future_years)
        for i in range(future_years):
            penalty, rebate = self.predict_feebate(env, n_oils[i], n_greens[i], self_n_oil, self_n_green, env.feebate_rate * (1 - FEEBATE_CHANGE_RATE) ** (i + 1))
            penalties[i] = penalty
            rebates[i] = rebate
        return penalties, rebates


class CustomEnv(base.Env):
    def __init__(self, *args, **kwargs):
        # self.feebate_rate_driver = 1 - args[6]
        self.feebate_rate_driver = args[6]
        super().__init__(*args, **kwargs)

    def update(self):
        super().update()
        self.feebate_rate_driver *= 1 - FEEBATE_CHANGE_RATE
        # self.feebate_rate = 1 - self.feebate_rate_driver
        self.feebate_rate = self.feebate_rate_driver


if __name__ == '__main__':
    INITIAL_FEEBATE_RATE = 1
    FEEBATE_CHANGE_RATE = 0.05
    sim = base.Simulation(CustomAgent, CustomEnv, initial_feebate_rate=INITIAL_FEEBATE_RATE)
    sim.run()
    sim.plot()
    sim.validate()