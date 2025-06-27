# 🤖 MBS Helper Bot

A powerful Telegram bot for automating YouTube updates, welcoming group members, admin broadcasts, and more.

---

## 📁 Project Structure

mbs_helper_bot/
├── main.py # Main bot logic
├── youtube_notify.py # YouTube update checker
├── keep_alive.py # Keeps bot alive (useful on Replit)
├── user_data.json # Stores chat/user IDs for broadcast
├── requirements.txt # Python package dependencies
├── README.md # You're here!
├── .env # (Not tracked) Holds sensitive info
└── .gitignore # Ignores .env, user_data.json, etc.

yaml
Copy
Edit

---

## ⚙️ 1. Setup Instructions

### ✅ Requirements

- Python 3.10 or higher  
- Telegram bot token via [@BotFather](https://t.me/BotFather)  
- Your Telegram user ID (for admin)  
- Optional: Your YouTube channel ID to fetch latest videos

---

## 🔐 2. `.env` File (Replace `config.py`)

Create a file named `.env` in the root folder with this content:

BOT_TOKEN=your-telegram-bot-token
ADMIN_ID=your-admin-id
CHANNEL_USERNAME=@yourchannelusername

yaml
Copy
Edit

> ⚠️ Don't commit this file to GitHub. It's already in `.gitignore`.

---

## 📦 3. Install Dependencies

Run this in your terminal:

```bash
pip install -r requirements.txt
▶️ 4. Run the Bot
Start the bot locally:

bash
Copy
Edit
python main.py
---
☁️ 5. Deploy (Optional)
You can host this bot on:

Replit

Add BOT_TOKEN, ADMIN_ID, CHANNEL_USERNAME as Replit secrets (not in .env)

PythonAnywhere

VPS or any Python-supported hosting

🛠 Features
Command	Description
/start	Show intro with inline buttons
/help	Show help message
/rules	Group rules
/adminpanel	Admin panel (only for authorized admin)
/broadcast	Broadcast message to all saved users (admin only)
/postchannel	Post message to a linked channel (admin only)
/users	Show total registered users
/delete	Delete last message (admin only)
➕ Auto-Welcome	Welcomes new users in group automatically
🔁 YouTube Update	Sends latest YouTube video notification to channel

📜 License
MIT — Free to use, modify, and share. Just don't remove credit 😉

✅ That’s it! You’re ready to go live.

yaml
Copy
Edit

---

### ✅ What Next?
- Paste this into `README.md` file
- Git add & commit:
  ```bash
  git add README.md
  git commit -m "📄 Added complete README with setup guide"
  git push
