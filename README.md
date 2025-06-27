## 🤖 MBS Helper Bot

A Telegram bot that sends YouTube video updates, helps users with group rules, allows admin broadcasts, and more.

---

### 📁 Project Structure

MBSHelperBot/
│
├── main.py # Main bot logic
├── config.py # Token and config values (NOT included in repo for security)
├── keep_alive.py # Keeps the bot alive on hosting platforms
├── youtube_notify.py # YouTube update checker
├── user_data.json # Stores chat IDs for broadcasting
├── requirements.txt # Python package dependencies
└── README.md # You're here!

yaml
Copy
Edit

---

### ⚙️ 1. Setup Instructions

#### ✅ Requirements

- Python 3.10+
- Telegram bot token from [BotFather](https://t.me/BotFather)
- Admin Telegram user ID
- Optional: A YouTube channel ID to track latest videos

---

### 🔐 2. `config.py` File (you must create this)

Create a file named `config.py` in the root folder with the following content:

```python
BOT_TOKEN = "your-telegram-bot-token"
ADMIN_ID = 123456789  # Replace with your Telegram user ID
CHANNEL_USERNAME = "@yourchannelusername"



📦 3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt



▶️ 4. Run the Bot
bash
Copy
Edit
python main.py



☁️ 5. Optional: Deploy to Replit or PythonAnywhere
Upload all files except user_data.json and config.py to a private project

On Replit, use .env or secret variables for token values instead of config.py

🛠 Features
/start – Show intro with inline buttons

/help – Show help message

/rules – Group rules

/adminpanel – Admin panel with buttons for broadcast, post, count

/broadcast – Admin-only broadcast to all saved users

/postchannel – Admin-only post to a configured Telegram channel

Auto-notify new members

Periodic check for new YouTube videos

📜 License
MIT – Use it, share it, modify it. Just don’t claim it's yours 😉

yaml
Copy
Edit

---

6. **Save the file**. That’s it!

Now when someone opens your project (or you zip it and send it), they can just open `README.md` and see full instructions.

Let me know if you want me to make the ZIP file for you next.