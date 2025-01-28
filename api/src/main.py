import logging
from src.controller.tarea import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import Config

config=Config()
logging.info(config.get("MONGODB"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(router)
