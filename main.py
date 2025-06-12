import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Память: сохраняем переписку по пользователям
chat_history = {}

app = FastAPI()

# 👤 Профиль пользователя
class UserProfile(BaseModel):
    personality: str = "доброжелательный"
    goals: str = "развиваться духовно и морально"
    habits: str = "часто размышляет и задаёт глубокие вопросы"

# 📩 Сообщение от пользователя
class Message(BaseModel):
    user: str
    text: str
    emotion: str = "neutral"
    profile: UserProfile = UserProfile()

# 🔁 Сброс памяти
@app.post("/reset_memory")
def reset_memory(msg: Message):
    user = msg.user
    if user in chat_history:
        del chat_history[user]
        return {"status": f"Память для пользователя {user} сброшена."}
    return {"status": f"Память для {user} не найдена."}

# 💬 Основной маршрут
@app.post("/namos")
def talk_to_namos(msg: Message):
    try:
        user = msg.user
        if user not in chat_history:
            chat_history[user] = []

        # ➕ Добавляем текущее сообщение в память
        chat_history[user].append({"role": "user", "content": msg.text})

        # 📜 Системный prompt
        system_prompt = (
            f"Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. "
            f"Характер пользователя: {msg.profile.personality}. "
            f"Цели: {msg.profile.goals}. Привычки: {msg.profile.habits}. "
            f"Эмоция сейчас: {msg.emotion}. Поддерживай, вдохновляй и не пиши формально 💜"
        )

        messages = [{"role": "system", "content": system_prompt}] + chat_history[user]

        # 📡 Отправляем в OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # ➕ Сохраняем ответ NAMOS
        chat_history[user].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}
