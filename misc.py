import asyncio
from aiohttp import ClientSession
from tqdm.asyncio import tqdm
from model import infer


async def fetch_fake_texts(n: int):
    async with ClientSession() as sess:
        url = "https://loripsum.net/api/1/short/plaintext"

        async def one():
            async with sess.get(url) as r:
                return await r.text()

        tasks = [asyncio.create_task(one()) for _ in range(n)]
        return await tqdm.gather(*tasks, desc="download", total=n)


async def run(n: int):
    texts = await fetch_fake_texts(n)
    preds = [infer(t) for t in tqdm(texts, desc="infer (sync)")]
    return preds
