## Medical Study Assistant Bot

A Telegram bot for medical students, powered by the ChatGPT API, with Telegram Scraper–based access control to ensure only authorized users can interact with the bot.
-----
## 📌 Overview

Medical Study Assistant Bot is a Telegram bot designed to help medical students with:

- 🧠 Quick medical explanations

- 📚 Summaries of medical topics

- 🩺 Clinical case understanding

- ❓ Q&A on anatomy, physiology, pathology, pharmacology, etc.

The bot uses OpenAI’s ChatGPT API to generate accurate, detailed responses and uses a Telegram Scraper to verify that each user is a valid member of an approved Telegram group or channel.
-----
## 🔐 Authorization Logic (Telegram Scraper)

To prevent unauthorized access, the bot checks:

If the user exists in a specific Telegram group/channel.

Access is only granted if:

- User is found in the scraped members list

- Or user ID is manually added to the allowed list

The scraper may:

- Fetch group members

- Store them locally (JSON/DB)

- Validate incoming users before processing messages

Unauthorized users receive a message telling them access is restricted.
------
🧰 Features
- ✔️ Medical Study Assistance

- Explain complex medical concepts

- Summarize long passages

- Provide definitions and clinical explanations

- Create study notes and quick revisions

- ✔️ ChatGPT API Integration

- Custom system prompt designed for medical accuracy

- Adjustable temperature and response styles

✔️ Telegram Bot Integration

- Handles messages using python-telegram-bot 

- Supports Markdown formatting

- Prevents non-authorized users from interacting

✔️ Telegram Scraper Access Control

- Scrapes group members using Pyrogram / Telethon

- Stores allowed IDs

- Checks each incoming message for authorization

  -----
  🚀 Getting Started
  1. Clone the repository
     
``` bash
  
 git clone https://github.com/yourusername/medical-study-bot.git
 cd medical-study-bot
 
 ```
  3. Install requirements
```bash
pip install -r requirements.txt
```
  5. Setup enviroment variables
```ini
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```
