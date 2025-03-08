from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from database import db_dependency
from security import check_password, MASTER_PASSWORD_HASH, hash_password
from models import User
from validators import add_user_dependency, delete_user_dependency

router = APIRouter(prefix="/users", tags=["users"])

templates = Jinja2Templates(directory="templates")


@router.get("/manage", status_code=status.HTTP_200_OK)
def manage_users(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_user(db: db_dependency, add_user_request: add_user_dependency):
    check_password(add_user_request.master_password, MASTER_PASSWORD_HASH)
    existing_user = db.query(User).filter_by(username=add_user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(add_user_request.password)
    user = User(username=add_user_request.username, password=hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse(content={"detail": "User added successfully"}, status_code=201)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, delete_user_request: delete_user_dependency):
    check_password(delete_user_request.master_password, MASTER_PASSWORD_HASH)
    user = db.query(User).filter_by(username=delete_user_request.username).first()
    if user:
        db.delete(user)
        db.commit()
        return JSONResponse(
            content={"detail": "User deleted successfully"}, status_code=200
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")
