import uvicorn
from src.routers import astrogpt
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(astrogpt.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
