from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated, BotCommand
from keep_alive import keep_alive

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatType
from config import BOT_TOKEN, ADMIN_ID, CHANNEL_USERNAME
import json
import asyncio
from youtube_notify import get_latest_video

# === Auto-reply dictionary ===
COMMON_QUESTIONS = {
    "rules": "📜 Group Rules:\n1. Respect Karo har Kisi Ki\n2. Spam or Scammer not Allowed\n3. Koi Promotion Ya irrelevent link nahi bhejna.",
    "admin": "👨‍💼 Admin: @mbshustler\nMasla ho to direct message karein.",
    "contact": "📩 Contact: mbsbusinesses1@gmail.com ya Telegram @mbshustler",
    "youtube": "📺 YouTube: https://www.youtube.com/@MBSKnowledgeHub"
}

# === Keyword checker ===
def get_keyword_response(user_message: str) -> str | None:
    message = user_message.lower()
    for keyword, reply in COMMON_QUESTIONS.items():
        if keyword in message:
            return reply
    return None

# === Auto keyword-based response handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        keyword_reply = get_keyword_response(update.message.text)
        if keyword_reply:
            await update.message.reply_text(keyword_reply)

# === Save Chat IDs for broadcast ===
def save_chat_id(chat_id):
    try:
        with open("user_data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if chat_id not in data:
        data.append(chat_id)
        with open("user_data.json", "w") as f:
            json.dump(data, f)

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❓ Help", callback_data='help')],
        [InlineKeyboardButton("📺 YouTube", url="https://www.youtube.com/@MBSKnowledgeHub")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/mbs_hub")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Assalamu Alaikum! Main MBS Helper Bot hoon. Niche buttons se madad lein:",
        reply_markup=reply_markup
    )
    save_chat_id(update.message.chat_id)

# === Button click handler ===
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await query.edit_message_text("🆘 Aap mujhse YouTube aur group-related madad le sakte hain. Commands use karein.")
    elif query.data == "admin_usercount":
        try:
            with open("user_data.json", "r") as f:
                chat_ids = json.load(f)
            await query.edit_message_text(f"📊 Total users/groups: {len(chat_ids)}")
        except:
            await query.edit_message_text("⚠️ Data file not found.")
    elif query.data == "admin_broadcast":
        await query.edit_message_text("✉️ Reply with: `/broadcast Your message here`", parse_mode="Markdown")
    elif query.data == "admin_post_channel":
        await query.edit_message_text("📢 Reply with: `/postchannel Your message here`", parse_mode="Markdown")

# === Greet New Members ===
async def greet_on_join(update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member.new_chat_member.user.id != context.bot.id:
        await context.bot.send_message(
            chat_id=update.chat.id,
            text=f"👋 Welcome {update.chat_member.new_chat_member.user.first_name} to the group!"
        )

# === Help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Commands:\n/start - Bot shuru karein\n/rules - Group rules\n/admin - Admin info")

# === Rules Command ===
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMON_QUESTIONS["rules"])

# === Admin Info Command ===
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMON_QUESTIONS["admin"])

# === Admin Panel Command ===
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("❌ Aap authorized admin nahi ho.")
        return

    keyboard = [
        [InlineKeyboardButton("🔁 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📢 Post to Channel", callback_data="admin_post_channel")],
        [InlineKeyboardButton("📊 User Count", callback_data="admin_usercount")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🛠️ *Admin Control Panel*", reply_markup=reply_markup, parse_mode="Markdown")

# === Broadcast Command ===
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Aap authorized admin nahi ho.")
        return

    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("📢 Use: /broadcast [your message]")
        return

    try:
        with open("user_data.json", "r") as f:
            chat_ids = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await update.message.reply_text("⚠️ Koi user data nahi mila.")
        return

    count = 0
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
            count += 1
        except:
            continue

    await update.message.reply_text(f"✅ Broadcast sent to {count} chats.")

# === Post to Channel Command ===
async def post_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Aap authorized admin nahi ho.")
        return

    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❗ Use: /postchannel [message]")
        return

    await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=msg)
    await update.message.reply_text("✅ Message sent to channel.")

# === User Count Command ===
async def user_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("user_data.json", "r") as f:
            chat_ids = json.load(f)
        await update.message.reply_text(f"👥 Total users: {len(chat_ids)}")
    except (FileNotFoundError, json.JSONDecodeError):
        await update.message.reply_text("⚠️ User data not found.")

# === Welcome new members ===
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"🎉 Welcome {member.first_name}! Abh aap Bhi MBS Hustler Ka Member Huwa Just Start Hustling!"
        )

# === Delete Last Message Command ===
async def delete_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Aap authorized admin nahi ho.")
        return

    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.message_id - 1
        )
        await update.message.delete()
    except:
        await update.message.reply_text("⚠️ Failed to delete previous message.")

# === YouTube Auto Notify ===
async def youtube_checker(app):
    while True:
        await asyncio.sleep(60 * 5)
        message = get_latest_video()
        if message:
            await app.bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode="Markdown")

# === Set Bot Commands ===
async def set_commands(application):
    commands = [
        BotCommand("start", "Bot ko start karein"),
        BotCommand("help", "Madad hasil karein"),
        BotCommand("rules", "Group rules"),
        BotCommand("admin", "Admin info"),
        BotCommand("broadcast", "Admin message broadcast"),
        BotCommand("postchannel", "Admin post to channel"),
        BotCommand("users", "Total registered users count"),
        BotCommand("delete", "Delete last message"),
        BotCommand("adminpanel", "Open admin panel")
    ]
    await application.bot.set_my_commands(commands)

# === Build App ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.post_init = lambda _: asyncio.create_task(youtube_checker(app))
app.post_init = set_commands

# === Register Handlers ===
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("rules", rules_command))
app.add_handler(CommandHandler("admin", admin_command))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("postchannel", post_to_channel))
app.add_handler(CommandHandler("users", user_count))
app.add_handler(CommandHandler("delete", delete_last))
app.add_handler(CommandHandler("adminpanel", admin_panel))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(ChatMemberHandler(greet_on_join, ChatMemberHandler.CHAT_MEMBER))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))

# ✅ Add keyword-based response handler
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

keep_alive()
print("🤖 Bot is running...")
app.run_polling()
