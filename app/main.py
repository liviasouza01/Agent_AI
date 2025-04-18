from fastapi import FastAPI
from app.routes.cotação import router as quote_router

app = FastAPI(title="AI Travel Assistant")

app.include_router(quote_router, prefix="/quote")
