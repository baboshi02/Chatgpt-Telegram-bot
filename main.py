import dotenv
import os
import telebot
import chatgpt
import base64
from firebase import db

dotenv.load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def validate_user(userId, collection_ref):
    pass


def main():
    client = chatgpt.GPT4TurboClient(CHATGPT_TOKEN, "gpt-4o")
    senders_ref = db.collection("users")
    # content_types = ['audio', 'photo', 'voice', 'video',
    #                  'document', 'text', 'location', 'contact', 'sticker']

    # TODO: add user addition via telegram

    @bot.message_handler(commands=["Hello", "Start"])
    def Greeting(message: telebot.types.Message):
        bot.reply_to(message, "Hello welcome to our chatgpt bot")

    @bot.message_handler(content_types=['photo'])
    def handle_images(message: telebot.types.Message):
        # encode image
        try:
            sender_id = str(message.from_user.id)
            doc_ref = senders_ref.document(sender_id)
            doc = doc_ref.get()
            # Get context history from db if it exists else initiate empty list
            context_history = doc.to_dict(
            )["context_history"] if doc.exists else []
            image_info = bot.get_file(message.photo[-1].file_id)
            downloaded_image = bot.download_file(image_info.file_path)
            encoded_image = base64.b64encode(downloaded_image).decode("utf-8")
            # Send Image with caption without context_history
            if (message.caption):
                chatgpt_response = client.send_b64_image_with_prompt(
                    encoded_image, message.caption)
                content = message.caption
            else:
                chatgpt_response = client.send_b64_image(encoded_image)
                content = " what is this image"

            bot.reply_to(message, chatgpt_response)
            add_to_context_history(
                content, chatgpt_response, doc_ref, context_history)

        except Exception as e:
            raise e
            bot.reply_to(message, "sorry error  occured")
            print(e)

    @bot.message_handler(func=lambda msg: True, content_types=['text'])
    def handle_text(message: telebot.types.Message):
        # TODO: extract the logic of converting to object to the chatgpt class
        message_length = len(message.text)
        max_length = 200
        if message_length > max_length:
            bot.reply_to(message, f"Message length must be less than 100 characters long \n Current length {
                message_length} ")
            return
        try:
            prompt = message.text
            sender_id = str(message.from_user.id)
            doc_ref = senders_ref.document(sender_id)
            doc = doc_ref.get()
            # Get context history from firebase if it exists else initiate empty list
            context_history = doc.to_dict(
            )["context_history"] if doc.exists else []
            chatgpt_response = client.send_text(prompt, context_history)
            bot.reply_to(message, chatgpt_response)
            add_to_context_history(
                prompt, chatgpt_response, doc_ref, context_history)
        except Exception as e:
            bot.reply_to(message, f"sorry {e} occured")
            print(e)
            raise e
    bot.infinity_polling()


def add_to_context_history(user_content, chatgpt_respones,  doc_ref, context_history, max_length=20):
    recent_user_context = {"role": "user", "content": user_content}
    recent_assisatnt_context = {
        "role": "assistant", "content": chatgpt_respones}
    context_history.append(recent_user_context)
    context_history.append(recent_assisatnt_context)
    if len(context_history) > max_length:
        context_history = context_history[max_length:]
    doc_ref.set({"context_history": context_history})


if __name__ == "__main__":
    print("Runinng.... ")
    main()
