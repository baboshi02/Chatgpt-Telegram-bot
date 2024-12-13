import json

import chatgpt

prompt = """
I have a dataset collected from Telegram (including messages, date, sender name ) and I’d like to leverage this information to better understand my audience, identify the most engaging content topics, and determine the best posting patterns. The ultimate goal is to develop a comprehensive media strategy and content plan that can be effectively applied across all other social media platforms.

What I need from you:

1. Analyze the provided dataset to identify audience interests, demographics (if possible), and the types of content that yield the highest engagement.


2. Determine the optimal posting times and content formats that best capture audience attention and encourage interaction.


3. Derive insights from Telegram user behavior and propose a content strategy that can be scaled and adapted across various platforms .


4. Suggest a holistic media plan that includes content types, posting schedules, and engagement tactics tailored to each platform and aligned with the target audience’s preferences.

"""

# response = chatgpt.prompting(prompt)

with open("sample.json", "r") as file:
    data = json.dumps(json.load(file), ensure_ascii=False)
response = chatgpt.prompting(prompt)
print("Chatgpt: ", response)
print("---------------------------")
response = chatgpt.prompting(data)
print("Chatgpt: ", response)
