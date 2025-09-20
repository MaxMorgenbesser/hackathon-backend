from fastapi import FastAPI
from src.routes import webhook
from dotenv import load_dotenv

app = FastAPI()


app.include_router(webhook.router)