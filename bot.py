import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7888027863:AAHBFNGcq3GAdVnobHWaELrB2SSRcn2Lhmk'
API_URL = 'https://fastapi-api-4mlu.onrender.com/namos'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "User"
    text = update.message.text

    data = {
        "user": user,
        "text": text
    }

    try:
        response = requests.post(API_URL, json=data)
        reply = response.json().get("reply", "⚠️ Ошибка при получении ответа.")
    except Exception as e:
        reply = f"⚠️ Ошибка запроса: {e}"

    await update.message.reply_text(reply)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен ✅")
    app.run_polling()
