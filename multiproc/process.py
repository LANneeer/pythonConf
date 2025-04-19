import asyncio
import multiprocessing as mp
from multiprocessing import Pool
from typing import List, Tuple

from telegram.app import TelegramBot
from model import embed


async def _collect_texts(limit: int, group: str | None) -> List[str]:
    bot = TelegramBot(msg_count=limit, group=group or "")
    async with bot.app:
        msgs = await bot.parse()
    return [content for _, _, content in msgs]


def _embed_batch(texts: List[str]) -> List[Tuple[float, float]]:
    return embed(texts)


def run(limit: int = 10, group: str | None = None) -> List[Tuple[float, float]]:
    mp.set_start_method("fork")
    texts = asyncio.run(_collect_texts(limit, group))
    with Pool(processes=1) as pool:
        coords, labels = pool.apply(_embed_batch, (texts,))

    return coords, labels
