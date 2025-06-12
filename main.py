import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Память: сохраняем переписку по пользователям
chat_history = {}

app = FastAPI()

class Message(BaseModel):
    user: str
    text: str

@app.post("/namos")
def talk_to_namos(msg: Message):

@app.post("/reset_memory")
def reset_memory(msg: Message):
    user = msg.user
    if user in chat_history:
        del chat_history[user]
        return {"status": f"Память для пользователя '{user}' сброшена."}
    return {"status": f"Память для '{user}' не найдена."}

    try:
        user = msg.user
        if user not in chat_history:
            chat_history[user] = []

        # Добавляем текущее сообщение пользователя в память
        chat_history[user].append({"role": "user", "content": msg.text})

        # Сообщения: system prompt + история
        messages = [
            {
                "role": "system",
                "content": "Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. Поддерживай, вдохновляй и не пиши слишком формально 💜"
            }
        ] + chat_history[user]

        # Отправка в OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Добавляем ответ NAMOS в память
        chat_history[user].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}
