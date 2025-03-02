from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from database import get_session
from security import check_password, MASTER_PASSWORD_HASH, hash_password
from models import User
from utils import execute_command, schedule_command, check_credentials, schedule_command_endpoint


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/webhook")
async def webhook(request: Request):
    return await execute_command("CD", request)


@router.get("/manage")
def manage_users(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})


@router.post("/add_user")
async def add_user(
    username: str = Form(...),
    password: str = Form(...),
    master_password: str = Form(...),
):
    if not check_password(master_password, MASTER_PASSWORD_HASH):
        return JSONResponse(
            content={"message": "Invalid master password"}, status_code=401
        )

    session = get_session()
    try:
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return JSONResponse(
                content={"message": "User already exists"}, status_code=400
            )

        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password)
        session.add(user)
        session.commit()
        return JSONResponse(
            content={"message": "User added successfully"}, status_code=201
        )
    except Exception as e:
        session.rollback()
        return JSONResponse(content={"message": "Failed to add user"}, status_code=500)
    finally:
        session.close()


@router.post("/delete_user")
async def delete_user(username: str = Form(...), master_password: str = Form(...)):
    if not check_password(master_password, MASTER_PASSWORD_HASH):
        return JSONResponse(
            content={"message": "Invalid master password"}, status_code=401
        )

    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
            return JSONResponse(
                content={"message": "User deleted successfully"}, status_code=200
            )
        else:
            return JSONResponse(content={"message": "User not found"}, status_code=404)
    except Exception as e:
        session.rollback()
        return JSONResponse(
            content={"message": "Failed to delete user"}, status_code=500
        )
    finally:
        session.close()


@router.post("/1am")
async def schedule_command_at_1am(request: Request):
    return await schedule_command_endpoint(request, "CD")
