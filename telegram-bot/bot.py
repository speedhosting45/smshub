import telegram
from telegram.ext import Updater, CommandHandler
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = telegram.Bot(token=config['bot_token'])
updater = Updater(token=config['bot_token'], use_context=True)

def start(update, context):
    update.message.reply_text("🕵️ SMS Spy Active")
    bot.send_message(chat_id=config['admin_chat_id'], text="✅ Bot is online!")

updater.dispatcher.add_handler(CommandHandler('start', start))
print("Bot running... No server needed!")
updater.start_polling()
updater.idle()
