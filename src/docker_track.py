import pandas as pd
import numpy as np
import docker
from matplotlib import pyplot as plt
import os
from datetime import datetime


def get_timestamp(format: str = "%Y-%m-%d_%H:%M:%S") -> str:
    return datetime.strftime(datetime.now(), format=format)


APPEND = False

client = docker.from_env()

containers = client.containers.list()
containers
print(f"containers: {containers}")

# names = [get_simple_name(c.name) for c in containers]
names = [c.name for c in containers]
print(f"names: {names}")


# %%

containers_to_watch = [
    # "automl-preprocessing-worker",
    # "automl-training-worker",
    # "automl-prediction-worker",
    "python-sandbox"
]


def main():
    # make archive of currently existing data
    tracking_file_path = "container_memory.csv"

    # if specified, append to existing tracking file, else cache existing file (if exists) and make a new one
    if APPEND:
        pass
    else:
        if os.path.exists(tracking_file_path):
            name, ext = tracking_file_path.split(".")
            new_path = "_".join([name, get_timestamp()]) + f".{ext}"
            os.rename(tracking_file_path, new_path)

        # create new tracking file
        mem_df = pd.DataFrame(columns=containers_to_watch + ["time_stamp"])
        mem_df.to_csv(tracking_file_path, index=False)

    mem_df = pd.read_csv(tracking_file_path)

    # running this cell sets up continuous monitoring of the data
    while True:
        memory_stats = {}
        for c in containers:
            if c.name not in containers_to_watch:
                continue

            container_stats = c.stats(stream=False)
            mem_mgb = container_stats["memory_stats"]["usage"] / 1024**2
            if (simp_name := c.name) not in memory_stats:
                memory_stats[simp_name] = [mem_mgb]
            else:
                memory_stats[simp_name].append(mem_mgb)

        # get time stamp (from most recent stats call)
        memory_stats["time_stamp"] = container_stats["read"]

        print(memory_stats["time_stamp"], memory_stats[simp_name])
        # append to dataframe
        mem_df = pd.concat([mem_df, pd.DataFrame(memory_stats)])

        # update file
        mem_df.to_csv(tracking_file_path, index=False)


if __name__ == "__main__":
    main()
