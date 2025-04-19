import os
from typing import List
import multiprocessing as mp
from aiomultiprocess import Pool

from telegram.app import TelegramBot
from model import embed


async def _collect_texts(limit: int, group: str | None) -> List[str]:
    bot = TelegramBot(msg_count=limit, group=group or "")
    async with bot.app:
        msgs = await bot.parse()
    return [text for _, _, text in msgs]


async def _embed(texts: List[str]):
    return embed(texts)


async def run(limit: int = 10, group: str | None = None):
    mp.set_start_method("fork")
    texts = await _collect_texts(limit, group)

    async with Pool(processes=os.cpu_count()) as pool:
        [(coords, labels)] = await pool.map(_embed, (texts,))
    return coords, labels
