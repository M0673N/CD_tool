from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher


load_dotenv()

# Get the master password and the command to be executed from .env file
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")
# Place your command in the .env file like this:
# COMMAND="cd path/to/docker-compose.yml && docker compose down --rmi && docker compose up -d"
command = os.getenv("COMMAND")
ph = PasswordHasher()
MASTER_PASSWORD_HASH = ph.hash(MASTER_PASSWORD)

engine = create_engine("sqlite:///users.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "credentials"
    username = Column(String, primary_key=True)
    password = Column(String)


Base.metadata.create_all(engine)

app = FastAPI()


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        return False


def check_credentials(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user:
        return check_password(password, user.password)
    else:
        return False


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if check_credentials(username, password):
        subprocess.run(command, shell=True, check=True)
        return {"message": "Command executed successfully"}
    else:
        return {"message": "Invalid credentials"}


@app.get("/manage")
def manage_users():
    html_content = """
    <html>
    <body>
        <h2>Manage Users</h2>
        <form action="/add_user" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br>
            <label for="master_password">Master Password:</label><br>
            <input type="password" id="master_password" name="master_password" required><br><br>
            <input type="submit" value="Add User">
        </form>
        <form action="/delete_user" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br>
            <label for="master_password">Master Password:</label><br>
            <input type="password" id="master_password" name="master_password" required><br><br>
            <input type="submit" value="Delete User">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/add_user")
async def add_user(
    username: str = Form(...),
    password: str = Form(...),
    master_password: str = Form(...),
):
    if not ph.verify(MASTER_PASSWORD_HASH, master_password):
        return {"message": "Invalid master password"}

    session = Session()
    try:
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password)
        session.add(user)
        session.commit()
        return {"message": "User added successfully"}
    except Exception as e:
        session.rollback()
        return {"message": "Failed to add user"}
    finally:
        session.close()


@app.post("/delete_user")
async def delete_user(username: str = Form(...), master_password: str = Form(...)):
    if not ph.verify(MASTER_PASSWORD_HASH, master_password):
        return {"message": "Invalid master password"}

    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}
    except Exception as e:
        session.rollback()
        return {"message": "Failed to delete user"}
    finally:
        session.close()

# Start command:
# uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Webhook usage example:
# curl -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d '{"username": "my_username", "password": "my_password"}'
# (you run this in the terminal)
