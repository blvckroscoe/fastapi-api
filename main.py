from pydantic import BaseModel

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
