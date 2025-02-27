import asyncio
import os
from time import time

import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("CHATGPT_TOKEN")


class ChatGptClient:
    def __init__(self, api_key, model="gpt-4-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def send_b64_image_with_prompt(self,  base64_image, prompt, context_history=[]):
        message = {"role": "user", "content": [
            {
                "type": "text",
                "text": prompt,
            }, {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}

            }
        ]}
        context_history.append(message)
        return self.send_to_chatgpt(context_history)

    def send_to_chatgpt(self, context_history, max_tokens=1000):
        response = openai.chat.completions.create(
            model=self.model,
            messages=context_history,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def send_b64_image(self, base64_image, context_history=[]):
        message = {"role": "user", "content": [{
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        }]
        }
        context_history.append(message)
        return self.send_to_chatgpt(context_history)

    def send_text(self, prompt, context_history=[], max_tokens=1000):
        message = {"role": "user", "content": prompt}
        context_history.append(message)
        return self.send_to_chatgpt(context_history, max_tokens)


# Example Usage
if __name__ == "__main__":
    CHATGPT_API_KEY = os.getenv("CHATGPT_TOKEN")
    client = ChatGptClient(CHATGPT_API_KEY)
    # Example long input text
    print("enter q to exit")
    context_history = []
    while True:
        prompt = input("Input prompt: ")
        if prompt.lower() == "q":
            print("bye")
            break
        try:
            response = client.send_text(prompt, context_history)
            print("Chatgpt: ", response)
            message = {"role": "user", "content": prompt}
            context_history.append(message)
            context_history.append({"role": "assistant", "content": response})
        except Exception as e:
            print("Error:", e)
