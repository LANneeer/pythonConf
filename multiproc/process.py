import os
import asyncio
import multiprocessing as mp
from multiprocessing import Pool
from typing import List, Tuple

from telegram.app import TelegramBot
from misc import fetch_fake_texts
from model import embed


def _collect_texts(limit: int, group: str | None) -> List[str]:
    # bot = TelegramBot(msg_count=limit, group=group or "")
    # with bot.app:
    #     msgs = bot.sync_parse()
    # return [content for _, _, content in msgs]
    texts = fetch_fake_texts(limit)
    return texts


def _embed_batch(texts: List[str]):
    return embed(texts)


def split_into_batches(texts: List[str], num_batches: int) -> List[List[str]]:
    batch_size = (len(texts) + num_batches - 1) // num_batches  # округление вверх
    return [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]


def run(limit: int = 10, group: str | None = None):
    mp.set_start_method("fork")
    texts = _collect_texts(limit, group)
    batches = split_into_batches(texts, num_batches=os.cpu_count())
    with Pool() as pool:
        results = pool.map(_embed_batch, batches)
    all_coords = [coord for batch in results for coord in batch[0]]
    all_texts = [text for batch in results for text in batch[1]]
    return all_coords, all_texts
