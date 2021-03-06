import random
import numpy as np
import pandas as pd
import numpy.random as rd
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm

from utils import EpsilonGreedy, UCB1, ThompsonSampling
from utils import BernoulliArm
from testdata import exponential


def test_algorithm(algo, arms, num_sims, horizon):
    chosen_arms = np.zeros(num_sims * horizon)
    rewards = np.zeros(num_sims * horizon)
    cumulative_rewards = np.zeros(num_sims * horizon)
    sim_nums = np.zeros(num_sims * horizon)
    times = np.zeros(num_sims * horizon)

    for sim in tqdm(range(num_sims)):
        sim = sim + 1
        algo.initialize(len(arms))

        for t in range(horizon):
            t = t + 1
            index = (sim - 1) * horizon + t - 1
            sim_nums[index] = sim
            times[index] = t
            chosen_arm = algo.select_arm()
            chosen_arms[index] = chosen_arm

            reward = arms[chosen_arm].draw()
            rewards[index] = reward

            if t == 1:
                cumulative_rewards[index] = reward
            else:
                cumulative_rewards[index] = cumulative_rewards[index - 1] + reward

            algo.update(chosen_arm, reward)

    return [sim_nums, times, chosen_arms, rewards, cumulative_rewards]


def run(algo, label):
    print(label)
    algo.initialize(n_arms)
    results = test_algorithm(algo, arms, num_sims=NUM_SIMS, horizon=HORIZON)

    df = pd.DataFrame({"times": results[1], "rewards": results[3]})
    grouped = df["rewards"].groupby(df["times"])
    plt.plot(grouped.mean(), label=label)
    plt.legend(loc="best")


if __name__ == '__main__':
    NUM_SIMS = 100
    # 選択数設定
    HORIZON = 1000
    # 試行回数設定

    # 問題設定: 腕：100本のうち、あたりは1つとする
    theta = np.array(exponential)
    n_arms = len(theta)

    arms = map(lambda x: BernoulliArm(x), theta)
    arms = list(arms)

    # EpsilonGreedyのepsilonの値設定
    algos = {
        'random': EpsilonGreedy([], [], epsilon=1),
        'Eps0.3': EpsilonGreedy([], [], epsilon=0.3),
        'Eps0.6': EpsilonGreedy([], [], epsilon=0.6),
        'UCB1': UCB1([], []),
        'TS': ThompsonSampling([], [])}
    for key, algo in algos.items():
        run(algo, label=key)

    # グラフを現在時刻をつけて保存
    now = datetime.datetime.now()
    plt.xlim(0, 1000)
    plt.ylim(-1, 1)
    plt.savefig('bandit' + str(now) + '.png')
