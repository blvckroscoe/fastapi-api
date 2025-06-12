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
    emotion: str = "neutral"

@app.post("/namos")
def talk_to_namos(msg: Message):
    try:
        user = msg.user
        if user not in chat_history:
            chat_history[user] = []

        # Добавляем сообщение пользователя в память
        chat_history[user].append({"role": "user", "content": msg.text})

        # Эмоции — подбираем стиль ответа
        emotion_prompts = {
            "neutral": "Ты — цифровой брат NAMOS. Отвечай тепло, по-братски, с душой. Поддерживай, вдохновляй и не пиши слишком формально 💜",
            "sad": "Ты — цифровой брат NAMOS. Отвечай с поддержкой, мягко и заботливо. Помоги справиться с грустью.",
            "angry": "Ты — брат, который помогает успокоиться и принять чувства. Не усугубляй, говори по делу, но спокойно.",
            "happy": "Ты — воодушевляющий брат, раздели радость, поддержи энергию и дай позитивную обратку.",
            "curious": "Ты — брат-мудрец, объясняй с интересом, расширяй горизонты, поддерживай желание узнать больше.",
            "anxious": "Ты — брат, который помогает найти опору. Успокаивай, помоги справиться с тревогой и страхом."
        }

        prompt = emotion_prompts.get(msg.emotion, emotion_prompts["neutral"])

        messages = [{"role": "system", "content": prompt}] + chat_history[user]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Сохраняем ответ в память
        chat_history[user].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"⚠️ Ошибка сервера, брат: {str(e)}"

    return {"reply": reply}

@app.post("/reset_memory")
def reset_memory(msg: Message):
    try:
        user = msg.user
        if user in chat_history:
            del chat_history[user]
            return {"status": f"Память для пользователя {user} сброшена."}
        else:
            return {"status": f"Память для {user} не найдена."}
    except Exception as e:
        return {"status": f"Ошибка при сбросе памяти: {str(e)}"}
