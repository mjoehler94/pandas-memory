import os

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("fivethirtyeight")


def animate(i):

    df = pd.read_csv("container_memory.csv")
    x = df.index

    plt.cla()

    max_mgb = 1
    for c in df.columns[:-1]:
        max_mgb = max(max_mgb, df[c].max())
        plt.plot(x, df[c], label=c)

    plt.ylabel("Megabytes", fontsize=13)
    plt.ylim(0, max_mgb + 1_000)
    plt.legend(loc="upper left")


try:
    print(os.getcwd())
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()
except:
    print("Fail")
