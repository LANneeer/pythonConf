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


def run(limit: int = 10, group: str | None = None) -> List[Tuple[float, float]]:
    mp.set_start_method("fork")
    texts = _collect_texts(limit, group)
    with Pool() as pool:
        coords, labels = pool.apply(_embed_batch, (texts,))
    return coords, labels
