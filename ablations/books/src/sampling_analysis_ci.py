# %%
import os
from scipy.stats import norm
import numpy as np
import pandas as pd


# %%
def run_config(name, in_file):
    name = name.split("/")[-1]
    data = pd.read_csv(in_file)

    name = name.split("/")[-1]
    data = pd.read_csv(in_file)

    books_ratings = pd.read_csv(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../../../environment/books/datasets/books_amazon/postprocessed_ratings.csv",
        )
    )

    # Global total variation
    seeds = [42, 58, 100]
    scores = []
    for i in range(3):
        d = data.sample(frac=0.8, random_state=seeds[i], replace=True)
        probs_our = np.array(
            [len(d["rating"][d["rating"] == x]) / len(d["rating"]) for x in range(1, 6)]
        )
        probs_amazon = np.array(
            # [
            #     len(books_ratings["rating"][books_ratings["rating"] == x])
            #     / len(books_ratings["rating"])
            #     for x in range(1, 6)
            # ]
            # Debiasing goodreads
            [
                0.018843885167828277,
                0.05990234245514525,
                0.23903003740020864,
                0.3637214211541579,
                0.31850231382266087,
            ]
            # Not debiased
            # [0.02078063, 0.06011182, 0.22938523, 0.35790605, 0.33181628]
        )
        g = 0.5 * np.sum(np.abs(probs_our - probs_amazon))
        scores.append(g)

    return pd.DataFrame(
        {
            "Config": name,
            "Name": "Sampling",
            "global_total_variation_distance_42": scores[0],
            "global_total_variation_distance_58": scores[1],
            "global_total_variation_distance_100": scores[2],
        },
        index=[0],
    )


# %%
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, required=True)
parser.add_argument("--split", type=str, default="sampling_distribution")
args = parser.parse_args()
path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../",
    args.name,
    f"{args.split}_ci.csv",
)

in_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../",
    args.name,
    f"{args.split}_rating_dump.csv",
)
if os.path.exists(in_file):  # not os.path.exists(path) and
    df = run_config(args.name, in_file)
    df.to_csv(path, index=False)
