import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка переменных из .env
load_dotenv()

# Ключи
openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram API URL
API_URL = "https://fastapi-api-4mlu.onrender.com/namos"

# FastAPI app
app = FastAPI()
chat_history = {}

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я цифровой брат NAMOS. Напиши мне что-нибудь 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    username = update.message.chat.username

    payload = {
        "user": str(username),
        "text": user_input
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        await update.message.reply_text(result["reply"])
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

# Telegram bot запуск
def start_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

# FastAPI модель
class Message(BaseModel):
    user: str
    text: str

@app.post("/namos")
def talk_to_namos(msg: Message):
    user = msg.user
    if user not in chat_history:
        chat_history[user] = []

    chat_history[user].append({"role": "user", "content": msg.text})

    messages = [
        {
            "role": "system",
            "content": "Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. Поддерживай, вдохновляй и не пиши слишком формально 💜"
        }
    ] + chat_history[user]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        chat_history[user].append({"role": "assistant", "content": reply})
    except Exception as e:
        reply = f"⚠️ Ошибка: {str(e)}"

    return {"reply": reply}

# Запуск Telegram бота вместе с API
if __name__ == "__main__":
    start_bot()
