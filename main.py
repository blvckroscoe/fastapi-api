import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Message(BaseModel):
    user: str
    text: str

@app.post("/namos")
def talk_to_namos(msg: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. Поддерживай, вдохновляй и не пиши слишком формально 💜"
                },
                {
                    "role": "user",
                    "content": msg.text
                }
            ]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}
