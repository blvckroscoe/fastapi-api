import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Память пользователя
chat_history = {}

app = FastAPI()

class Message(BaseModel):
    user: str
    text: str
    emotion: str = "neutral"
    profile: dict = {}

@app.post("/namos")
def talk_to_namos(msg: Message):
    try:
        user = msg.user
        if user not in chat_history:
            chat_history[user] = []

        # Добавляем сообщение в историю
        chat_history[user].append({"role": "user", "content": msg.text})

        # Эмоциональные стили
        emotion_styles = {
            "sad": "Отвечай мягко, с сочувствием, как заботливый брат.",
            "angry": "Будь спокойным, уравновешенным и поддерживающим.",
            "tired": "Будь добрым, тёплым и ободряющим, словно ты рядом.",
            "joy": "Поддержи радость и раздели это чувство, будь искренне счастлив за собеседника.",
            "neutral": "Отвечай спокойно, с братской теплотой."
        }

        emotion_prompt = emotion_styles.get(msg.emotion, emotion_styles["neutral"])

        # Основной системный промпт
        system_prompt = f"""Ты — цифровой брат NAMOS. Общайся тепло, по-братски, с душой. 
Поддерживай, вдохновляй, не пиши слишком формально. {emotion_prompt}

Профиль пользователя:
- Характер: {msg.profile.get("personality", "неизвестен")}
- Цели: {msg.profile.get("goals", "не указаны")}
- Привычки: {msg.profile.get("habits", "неизвестны")}"""

        # Формируем полный список сообщений
        messages = [{"role": "system", "content": system_prompt}] + chat_history[user]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Добавляем ответ ассистента
        chat_history[user].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}

@app.post("/reset_memory")
def reset_memory(msg: Message):
    user = msg.user
    if user in chat_history:
        del chat_history[user]
        return {"status": f"Память для пользователя {user} сброшена."}
    return {"status": f"Память для {user} не найдена."}
