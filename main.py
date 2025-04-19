import argparse
import asyncio
import importlib
import time
from collections.abc import Sequence
from typing import List, Tuple
import matplotlib.pyplot as plt
from tqdm import tqdm

PIPELINES = {
    "asynchron": ("asynchron.process", True),
    "multiproc": ("multiproc.process", False),
    "aiomultiproc": ("aiomultiproc.process", True),
}


def visualize(coords: List[Tuple[float, float]], labels: List[str]):
    xs, ys = zip(*coords)
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(xs, ys, c=range(len(coords)), cmap="plasma", s=60, alpha=0.8)

    annot = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(10, 10),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->"),
    )
    annot.set_visible(False)

    def update_annot(ind):
        index = ind["ind"][0]
        pos = scatter.get_offsets()[index]
        annot.xy = pos
        text = labels[index][:80].replace("\n", " ") + (
            "..." if len(labels[index]) > 80 else ""
        )
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.9)

    def on_hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            elif vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    ax.set_title("t‑SNE Embeddings of Telegram Messages")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    plt.tight_layout()
    plt.show()


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
