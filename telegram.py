import json
import os

from dotenv import load_dotenv
from telethon import TelegramClient

from utils import get_prev_month

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
# groupID = -1001760560044
groupID = -4538347316
client = TelegramClient("anon", API_ID, API_HASH)


async def main():
    telegramData = []
    # You can print the message history of any chat:
    two_months_back = get_prev_month(2)
    async for message in client.iter_messages(groupID, reverse=True, limit=10):
        try:
            messageDate = message.date
            messageText = message.text
            senderID = message.from_id.user_id
            sender = await message.get_sender()
            senderName = sender.username
        except Exception:
            print("error reading message")
            continue
        if not messageText or "None" in messageText:
            continue
        print("date: ", messageDate)
        print("text: ", messageText)
        print("id: ", senderID)
        print("sender", senderName)
        telegramData.append(
            {
                "date": messageDate,
                "text": messageText,
                "senderID": senderID,
                "senderName": senderName,
            }
        )

    json_object = json.dumps(telegramData, ensure_ascii=False, indent=4, default=str)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
        # You can download media from messages, too!
        # The method will return the path where the file was saved.


with client:
    client.loop.run_until_complete(main())
