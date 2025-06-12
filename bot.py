from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://fastapi-api-4mlu.onrender.com/namos"
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я цифровой брат NAMОS. Напиши мне что-нибудь 🧠")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    username = update.message.chat.username or update.message.chat.id

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

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Bot started...")
    app.run_polling()
