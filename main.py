import argparse
import asyncio
import importlib
import time
from collections.abc import Sequence
from typing import List, Tuple
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm

PIPELINES = {
    "asynchron": ("asynchron.process", True),
    "multiproc": ("multiproc.process", False),
    "aiomultiproc": ("aiomultiproc.process", True),
}


def visualize(
    coords: Sequence[Tuple[float, float]],
    labels: Sequence[str],
    *,
    title: str = "t‑SNE Embeddings of Telegram Messages",
    marker_size: int = 10,
    color_scale: str = "Plasma",
):
    if len(coords) == 0:
        raise ValueError("coords не должен быть пустым")
    if len(coords) != len(labels):
        raise ValueError("coords и labels должны быть одинаковой длины")

    xs, ys = np.array(coords).T
    df = {
        "x": xs,
        "y": ys,
        "idx": np.arange(len(coords)),
        "label": labels,
    }

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="idx",
        color_continuous_scale=color_scale,
        hover_name="label",
        height=650,
        width=900,
    )

    fig.update_traces(marker=dict(size=marker_size, opacity=0.8, line=dict(width=0)))
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white",
        coloraxis_showscale=False,
    )

    fig.show()


def main():
    parser = argparse.ArgumentParser(
        description="ETL demo: Telegram → t‑SNE embedding (asyncio & multiprocessing)"
    )
    parser.add_argument("--mode", choices=PIPELINES, default="aiomultiproc")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--group", default=None)
    args = parser.parse_args()

    module_name, is_async = PIPELINES[args.mode]
    mod = importlib.import_module(module_name)

    print(f"Running {args.mode} on {args.n} Telegram messages…")
    t0 = time.perf_counter()

    if is_async:
        coords, labels = asyncio.run(mod.run(args.n, args.group))
    else:
        coords, labels = mod.run(args.n, args.group)

    dt = time.perf_counter() - t0

    print(f"\n{args.mode} finished in {dt:.2f} seconds.\n")

    visualize(coords, labels)


if __name__ == "__main__":
    main()
