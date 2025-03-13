import uvicorn
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routes import webhook, users
from database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(content={"detail": "The server is working"}, status_code=200)


app.include_router(webhook.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="ssl/server.key",
        ssl_certfile="ssl/server.crt",
        workers=4,
    )
