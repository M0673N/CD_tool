import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import webhook, users
from database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(webhook.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4, reload=True)
