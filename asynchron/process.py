import asyncio
from typing import List

from telegram.app import TelegramBot
from model import embed


async def _collect_texts(limit: int, group: str | None) -> List[str]:
    bot = TelegramBot(msg_count=limit, group=group or "")
    async with bot.app:
        msgs = await bot.parse()
    return [text for _, _, text in msgs]


async def run(limit: int = 10, group: str | None = None):
    texts = await _collect_texts(limit, group)
    loop = asyncio.get_running_loop()
    coords, labels = await loop.run_in_executor(None, embed, texts)
    return coords, labels
