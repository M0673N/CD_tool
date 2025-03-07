import os
import subprocess
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from security import check_password, MASTER_PASSWORD_HASH, hash_password
from models import User, ScheduledJob
from database import db_dependency, SessionLocal
from validators import ExecuteCommandRequest, ScheduleCommandRequest


router = APIRouter(prefix="/webhook", tags=["webhook"])

load_dotenv()

scheduler = BackgroundScheduler()
scheduler.start()


@router.post("/", status_code=status.HTTP_200_OK)
async def webhook(db: db_dependency, execute_command_request: ExecuteCommandRequest):
    return execute_command(execute_command_request, db)


@router.post("/schedule", status_code=status.HTTP_200_OK)
async def schedule_command_at_1am(
    db: db_dependency, schedule_command_request: ScheduleCommandRequest
):
    return schedule_command_endpoint(schedule_command_request, db)


def run_command(cmd):
    command = os.getenv(cmd)
    if command is None:
        raise HTTPException(status_code=400, detail="This command is not allowed")
    subprocess.run(command, shell=True, check=True)


def check_credentials(username, password, db):
    user = db.query(User).filter_by(username=username).first()
    if user:
        return check_password(password, user.password)
    raise HTTPException(status_code=401, detail="Invalid credentials")


def execute_command(execute_command_request, db):
    check_credentials(
        execute_command_request.username, execute_command_request.password, db
    )
    run_command(execute_command_request.command)
    return JSONResponse(
        content={"detail": "Command executed successfully"}, status_code=200
    )


def schedule(job_name, hour, minute, db):
    trigger = CronTrigger(hour=hour, minute=minute)
    job = scheduler.add_job(
        run_scheduled_command, trigger=trigger, args=(job_name, hour, minute)
    )
    new_job = ScheduledJob(id=job.id, name=job_name, hour=hour, minute=minute)
    db.add(new_job)
    db.commit()
    return JSONResponse(
        content={"detail": f"Command scheduled for {hour}:{minute}"},
        status_code=200,
    )


def run_scheduled_command(job_name, hour, minute):
    db = SessionLocal()
    run_command(job_name)
    job_to_remove = (
        db.query(ScheduledJob)
        .filter_by(name=job_name, hour=hour, minute=minute)
        .first()
    )
    if job_to_remove:
        scheduler.remove_job(job_to_remove.id)
        db.delete(job_to_remove)
        db.commit()
    db.close()


def schedule_command(job_name, hour, minute, db):
    existing_job = (
        db.query(ScheduledJob)
        .filter_by(name=job_name, hour=hour, minute=minute)
        .first()
    )
    if not existing_job:
        return schedule(job_name, hour, minute, db)

    raise HTTPException(
        status_code=400,
        detail=f"Command already scheduled for {hour}:{minute}",
    )


def schedule_command_endpoint(schedule_command_request, db):
    check_credentials(
        schedule_command_request.username, schedule_command_request.password, db
    )
    return schedule_command(
        schedule_command_request.command,
        schedule_command_request.hour,
        schedule_command_request.minute,
        db,
    )
