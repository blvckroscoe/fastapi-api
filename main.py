import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Память по пользователям
chat_history = {}

# Инициализация FastAPI
app = FastAPI()

# Модель входящих данных
class Message(BaseModel):
    user: str
    text: str
    emotion: str = "neutral"  # по умолчанию нейтральная эмоция

@app.post("/namos")
def talk_to_namos(msg: Message):
    try:
        user = msg.user
        if user not in chat_history:
            chat_history[user] = []

        # Сохраняем сообщение пользователя
        chat_history[user].append({"role": "user", "content": msg.text})

        # Настраиваем эмоциональный стиль ответа
        emotion_instruction = {
            "neutral": "",
            "sad": "Если пользователь грустит, утешь его, поддержи и напомни, что он не один.",
            "angry": "Если он зол — успокой мягко, не спорь, направь на осознанность.",
            "happy": "Если он радуется — раздели радость!",
            "anxious": "Если тревожится — помоги найти стабильность.",
            "curious": "Если он задаёт вопрос с любопытством — вдохнови копать глубже!",
        }.get(msg.emotion, "")

        # Формируем сообщение с системной инструкцией
        messages = [
            {
                "role": "system",
                "content": f"Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. {emotion_instruction}"
            }
        ] + chat_history[user]

        # Запрос в OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Сохраняем ответ ассистента
        chat_history[user].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}

@app.post("/reset_memory")
def reset_memory(msg: Message):
    user = msg.user
    if user in chat_history:
        del chat_history[user]
        return {"status": f"Память для пользоват
