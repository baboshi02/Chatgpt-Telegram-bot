
import dotenv
import os
import telebot
import chatgpt
import tiktoken
import base64
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

    @bot.message_handler(content_types=['photo'])
    def handle_images(message):
        image_info = bot.get_file(message.photo[-1].file_id)
        downloaded_image = bot.download_file(image_info.file_path)
        # encode image
        encoded_image = base64.b64encode(downloaded_image).decode("utf-8")

    @bot.message_handler(func=lambda msg: True, content_types=content_types)
    def chatgpt_response(message: telebot.types.Message):
        print(message)
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
