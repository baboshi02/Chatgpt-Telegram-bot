
import dotenv
import os
import telebot
import chatgpt
import tiktoken
dotenv.load_dotenv()

BABOSHI_BOT_TOKEN = os.getenv("BABOSHI_BOT_TOKEN")
CHATGPT_API_KEY = os.getenv("CHATGPT_API")
bot = telebot.TeleBot(BABOSHI_BOT_TOKEN)


def main():
    client = chatgpt.GPT4TurboClient(CHATGPT_API_KEY, "gpt-4o")
    content_types = ['audio', 'photo', 'voice', 'video',
                     'document', 'text', 'location', 'contact', 'sticker']

    @bot.message_handler(commands=["Hello", "Start"])
    def Greeting(message: telebot.types.Message):
        bot.reply_to(message, "Hello welcome to our chatgpt bot")

    @bot.message_handler(func=lambda msg: True, content_types=content_types)
    def chatgpt_response(message: telebot.types.Message):
        try:
            response = client.chat(prompt=message.text)
            print(response)
            bot.reply_to(message, response)
        except Exception as e:
            bot.reply_to(message, f"sorry {e} occured")
            print(e)
            pass

    bot.infinity_polling()


if __name__ == "__main__":
    print("Runinng.... ")
    main()
