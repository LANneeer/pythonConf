import os
from typing import List
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()


class TelegramBot:
    def __init__(self, msg_count=10, group="") -> None:
        self.api_id = int(os.getenv("API_ID", 0))
        self.api_hash = str(os.getenv("API_HASH", ""))
        self.app_name = str(os.getenv("APP_NAME", ""))
        self.group = group
        self.limit = msg_count

        assert self.api_id != 0, "API_ID не задан"
        assert self.api_hash, "API_HASH не задан"
        assert self.app_name, "APP_NAME не задан"

        self.app = Client(self.app_name, api_id=self.api_id, api_hash=self.api_hash)

    async def parse(self) -> List:
        messages = []
        async for msg in self.app.get_chat_history(self.group, limit=self.limit):
            if msg.from_user:
                sender = msg.from_user.first_name
            elif msg.sender_chat:
                sender = msg.sender_chat.title
            else:
                sender = "Unknown"

            if msg.text:
                content = msg.text
            elif msg.caption:
                content = msg.caption
            elif msg.photo:
                content = "📷 Фото"
            elif msg.video:
                content = "🎥 Видео"
            elif msg.document:
                content = f"📎 Документ: {msg.document.file_name}"
            elif msg.sticker:
                content = f"💬 Стикер: {msg.sticker.emoji or '[sticker]'}"
            else:
                content = "[неизвестный тип сообщения]"

            messages.append((msg.date, sender, content))
        return messages

    def sync_parse(self) -> List:
        messages = []

        for msg in self.app.get_chat_history(self.group, limit=self.limit):
            if msg.from_user:
                sender = msg.from_user.first_name
            elif msg.sender_chat:
                sender = msg.sender_chat.title
            else:
                sender = "Unknown"

            if msg.text:
                content = msg.text
            elif msg.caption:
                content = msg.caption
            elif msg.photo:
                content = "📷 Фото"
            elif msg.video:
                content = "🎥 Видео"
            elif msg.document:
                content = f"📎 Документ: {msg.document.file_name}"
            elif msg.sticker:
                content = f"💬 Стикер: {msg.sticker.emoji or '[sticker]'}"
            else:
                content = "[неизвестный тип сообщения]"

            messages.append((msg.date, sender, content))

        return messages
