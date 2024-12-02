from fastapi import FastAPI
from app.views import router as book_router
from app.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_db_and_tables()

app.include_router(book_router)
