from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет, братец! API работает 🔥"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Ассаламу алейкум, {name}!"}
