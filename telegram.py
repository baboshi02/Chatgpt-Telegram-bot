import os

import dotenv
from telethon import TelegramClient

dotenv.load_dotenv()
API_ID = os.getenv("AMAR_TELEGRAM_API_ID")
API_HASH = os.getenv("AMAR_TELEGRAM_API_HASH")
PHONE_NUMBER = os.getenv("AMAR_PHONE_NUMBER")

CHAT_ID = int(os.getenv("CLUB_CHAT_ID"))


class TelegramScraper:
    def __init__(self, api_id: int, api_hash: str, phone_number: str):
        """
        Initialize the TelegramScraper class.

        :param api_id: Your Telegram API ID
        :param api_hash: Your Telegram API Hash
        :param phone_number: Your phone number registered with Telegram
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient("session_name", api_id, api_hash)

    async def connect(self):
        """
        Connects to the Telegram server and starts the client.
        """
        await self.client.start(phone=self.phone_number)

    async def get_participants(self, chat_name: str):
        """
        Fetch participants from a channel or group.

        :param chat_name: The username or ID of the channel/group.
        :return: A list of participants.
        """
        participants = await self.client.get_participants(chat_name)
        return participants

    async def get_messages(self, chat_name: str, limit: int = 100):
        """
        Fetch messages from a channel or group.

        :param chat_name: The username or ID of the channel/group.
        :param limit: The maximum number of messages to fetch.
        :return: A list of messages.
        """
        messages = await self.client.get_messages(chat_name, limit=limit)
        return messages

    async def get_media(self, chat_name: str, output_folder: str, limit: int = 100):
        """
        Download media files from a channel or group.

        :param chat_name: The username or ID of the channel/group.
        :param output_folder: The folder to save the downloaded media files.
        :param limit: The maximum number of media messages to fetch.
        """
        messages = await self.client.get_messages(chat_name, limit=limit)
        for msg in messages:
            if msg.media:
                await self.client.download_media(msg, file=output_folder)

    async def disconnect(self):
        """
        Disconnects the client from Telegram.
        """
        await self.client.disconnect()


# Example usage:
# Ensure you have your API credentials from https://my.telegram.org
if __name__ == "__main__":
    import asyncio

    scraper = TelegramScraper(API_ID, API_HASH, PHONE_NUMBER)

    async def main():
        await scraper.connect()

        messages = await scraper.get_messages(
            CHAT_ID, limit=50
        )  # Fetch the last 50 messages
        for msg in messages:
            print(msg.text)

        await scraper.disconnect()

    asyncio.run(main())
