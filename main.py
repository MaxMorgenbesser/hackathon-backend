from fastapi import FastAPI
from src.routes import webhook, prompt, history
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


app.include_router(webhook.router)
app.include_router(prompt.router)
app.include_router(history.router)