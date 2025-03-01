import os
import subprocess
from dotenv import load_dotenv
from fastapi import Request
from database import get_session
from models import User
from security import check_password, MASTER_PASSWORD_HASH, hash_password
from fastapi.responses import JSONResponse


load_dotenv()


def run_command(cmd):
    command = os.getenv(cmd)
    subprocess.run(command, shell=True, check=True)


def check_credentials(username, password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user:
        return check_password(password, user.password)
    else:
        return False


async def execute_command(command_name: str, request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if check_credentials(username, password):
        run_command(command_name)
        return JSONResponse(
            content={"message": "Command executed successfully"}, status_code=200
        )
    else:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)
