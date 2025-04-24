# src/prediction.py

import random
import numpy as np
from .utils import DISCOUNT_RATE

def predict_n_future(agent, env, agents, past_years, future_years):
    """
    過去past_years年間の特徴量を用いて、未来future_years年後の船の数を予測する
    （元の Agent.predict_n_future のロジックを移植）
    """
    predict_sum_n_oils   = np.zeros(future_years)
    predict_sum_n_greens = np.zeros(future_years)

    for other in agents:
        if other.ind == agent.ind:
            continue

        new_buy_oils   = np.zeros(future_years)
        new_buy_greens = np.zeros(future_years)
        for i in range(future_years):
            if len(other.history_green) == 0:
                # 履歴がなければランダム
                if i == 0:
                    buy_oil, buy_green = random.randint(0, 5), random.randint(0, 5)
                else:
                    buy_oil, buy_green = new_buy_oils[i-1], new_buy_greens[i-1]
            elif len(other.history_green) < past_years:
                # データ不足時は履歴平均
                buy_oil   = sum(other.history_oil)   / len(other.history_oil)
                buy_green = sum(other.history_green) / len(other.history_green)
            else:
                # 過去past_years年のデータ＋前回予測で平均
                if i == 0:
                    buy_oil   = sum(other.history_oil[-past_years:])   / past_years
                    buy_green = sum(other.history_green[-past_years:]) / past_years
                else:
                    hist_oil  = other.history_oil[-(past_years - i):]   if past_years - i > 0 else []
                    hist_green= other.history_green[-(past_years - i):] if past_years - i > 0 else []
                    fore_oil  = new_buy_oils[:i].tolist()
                    fore_green= new_buy_greens[:i].tolist()
                    comb_oil   = hist_oil   + fore_oil
                    comb_green = hist_green + fore_green
                    if comb_oil:
                        buy_oil   = sum(comb_oil)   / len(comb_oil)
                        buy_green = sum(comb_green) / len(comb_green)
                    else:
                        buy_oil, buy_green = 0, 0

            new_buy_oils[i]   = buy_oil
            new_buy_greens[i] = buy_green

        predict_sum_n_oils   += new_buy_oils
        predict_sum_n_greens += new_buy_greens

    # 全体数に加算して返す
    return (
        env.total_n_oil   + predict_sum_n_oils,
        env.total_n_green + predict_sum_n_greens
    )

def predict_feebate(agent, env, n_oil, n_green, self_n_oil, self_n_green, feebate_rate=None):
    """
    単年分のペナルティ／リベートを計算
    """
    rate = env.feebate_rate if feebate_rate is None else feebate_rate
    if n_oil == 0:
        return 0.0, 0.0
    penalty = self_n_oil * (env.p_green - env.p_oil * rate) * (n_green / n_oil)
    rebate  = self_n_green * (env.p_green - env.p_oil * rate)
    return max(0.0, penalty), max(0.0, rebate)

def predict_feebate_future(agent, env, n_oils, n_greens, self_n_oil, self_n_green, future_years):
    """
    future_years 年分のペナルティ／リベート配列を返す
    """
    penalties = np.zeros(future_years)
    rebates   = np.zeros(future_years)
    for i in range(future_years):
        p, r = predict_feebate(agent, env, n_oils[i], n_greens[i], self_n_oil, self_n_green)
        penalties[i] = p
        rebates[i]   = r
    return penalties, rebates
