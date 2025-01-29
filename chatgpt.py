import asyncio
import os
from time import time

import openai
from dotenv import load_dotenv
import tiktoken

load_dotenv()

OPENAI_API_KEY = os.getenv("AMAR_BOT_CHATGPT")


class GPT4TurboClient:
    def __init__(self, api_key, model="gpt-4-turbo"):
        """Initialize the GPT-4 Turbo client. :param api_key: Your OpenAI API key.
        :param model: The model to use (e.g., 'gpt-4-turbo').
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def count_tokens(self, text):
        """
        Count the number of tokens in a given text using tiktoken.
        :param text: The input text.
        :return: The number of tokens.
        """
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    def chunk_text(self, text, chunk_size):
        """
        Split the input text into chunks of a specific token size.
        :param text: The input text.
        :param chunk_size: The number of tokens per chunk.
        :return: A list of text chunks.
        """
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)
        chunks = [tokens[i: i + chunk_size]
                  for i in range(0, len(tokens), chunk_size)]
        return [encoding.decode(chunk) for chunk in chunks]

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

    def send_text(self, prompt, context_history=[]):
        message = {"role": "user", "content": prompt}
        context_history.append(message)
        return self.send_to_chatgpt(context_history)

    async def process_large_text(
        self, text, outfile, chunk_size=10000, max_tokens=1000, rate_limit=3
    ):
        """
        Process a large text by splitting it into chunks and sending each chunk to the model.
        :param text: The large input text.
        :param chunk_size: The number of tokens per chunk.
        :param max_tokens: The maximum number of tokens in the output per chunk.
        :return: A list of responses for each chunk.
        """
        chunks = self.chunk_text(text, chunk_size)
        responses = []
        start_time = time()
        for i, chunk in enumerate(chunks):

            elapsed_time = time() - start_time
            # If more than `rate_limit` prompts have been sent, wait for the remaining time
            if i > 0 and i % rate_limit == 0:
                wait_time = max(
                    0, 120 - elapsed_time
                )  # Wait for a full minute before resuming
                if wait_time > 0:
                    print(f"Rate limit reached. Waiting for {
                          wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
                    start_time = time()  # Reset the start time after waiting

            print(f"Processing chunk {i + 1}/{len(chunks)}...")
            response = self.chat(chunk, max_tokens=max_tokens)
            responses.append(response)
        return responses


# Example Usage
if __name__ == "__main__":
    CHATGPT_API_KEY = os.getenv("CHATGPT_API")
    client = GPT4TurboClient(CHATGPT_API_KEY)
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
