import asyncio
from aiohttp import ClientSession
import requests
from tqdm.asyncio import tqdm as tqdm_async
from tqdm import tqdm as tqdm_sync

FAKER_URL = "https://fakerapi.it/api/v1/texts"
MAX_BATCH = 1000


async def fetch_fake_texts_async(n: int):
    texts = []
    batches = (n + MAX_BATCH - 1) // MAX_BATCH

    async with ClientSession() as sess:

        async def fetch_batch(batch_size: int):
            params = {"_quantity": batch_size, "_characters": 120}
            async with sess.get(FAKER_URL, params=params) as r:
                r.raise_for_status()
                data = await r.json()
                return [item["content"] for item in data["data"]]

        tasks = [
            asyncio.create_task(fetch_batch(min(MAX_BATCH, n - i * MAX_BATCH)))
            for i in range(batches)
        ]

        results = await tqdm_async.gather(*tasks, desc="download", total=len(tasks))
        for batch in results:
            texts.extend(batch)

    return texts[:n]


def fetch_fake_texts(n: int):
    """
    Синхронная загрузка n фейковых текстов с fakerapi.it (requests)
    """
    texts = []
    batches = (n + MAX_BATCH - 1) // MAX_BATCH

    for i in tqdm_sync(range(batches), desc="download"):
        qty = min(MAX_BATCH, n - i * MAX_BATCH)
        params = {"_quantity": qty, "_characters": 120}
        r = requests.get(FAKER_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        texts.extend([item["content"] for item in data["data"]])

    return texts[:n]
