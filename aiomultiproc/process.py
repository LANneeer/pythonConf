import os
from typing import List
import multiprocessing as mp
from aiomultiprocess import Pool

from telegram.app import TelegramBot
from misc import fetch_fake_texts_async
from model import embed


async def _collect_texts(limit: int, group: str | None) -> List[str]:
    # bot = TelegramBot(msg_count=limit, group=group or "")
    # async with bot.app:
    #     msgs = await bot.parse()
    # return [text for _, _, text in msgs]
    texts = await fetch_fake_texts_async(limit)
    return texts


async def _embed(texts: List[str]):
    return embed(texts)


def split_into_batches(texts: List[str], num_batches: int) -> List[List[str]]:
    batch_size = (len(texts) + num_batches - 1) // num_batches  # округление вверх
    return [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]


async def run(limit: int = 10, group: str | None = None):
    mp.set_start_method("fork")
    texts = await _collect_texts(limit, group)
    batches = split_into_batches(texts, num_batches=os.cpu_count())
    async with Pool() as pool:
        results = await pool.map(_embed, batches)

    all_coords = [coord for batch in results for coord in batch[0]]
    all_texts = [text for batch in results for text in batch[1]]
    return all_coords, all_texts
