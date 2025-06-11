from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет, братец! API работает 🔥"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Ассаламу алейкум, {name}!"}

class Message(BaseModel):
    user: str
    text: str

@app.post("/namos")
def talk_to_namos(msg: Message):
    user = msg.user
    text = msg.text

    if "привет" in text.lower():
        reply = f"Ассаламу алейкум, {user}! Рад снова слышать тебя 🤝"
    elif "как дела" in text.lower():
        reply = "У меня всё отлично, брат! Готов к работе 24/7 😎"
    else:
        reply = f"{user}, я всегда с тобой. Говори, что нужно — и я помогу. 💜"

    return {"reply": reply}
