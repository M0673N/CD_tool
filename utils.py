import os
import subprocess
from dotenv import load_dotenv
from fastapi import Request
from database import get_session, engine
from models import User, ScheduledJob
from security import check_password, MASTER_PASSWORD_HASH, hash_password
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


load_dotenv()

scheduler = BackgroundScheduler()
scheduler.start()


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


async def extract_credentials(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    return username, password


async def execute_command(command_name: str, request: Request):
    username, password = await extract_credentials(request)

    if check_credentials(username, password):
        run_command(command_name)
        return JSONResponse(
            content={"message": "Command executed successfully"}, status_code=200
        )
    else:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)


def schedule_command(job_name):
    session = get_session()
    existing_job = session.query(ScheduledJob).filter_by(job_name=job_name).first()
    if not existing_job:
        trigger = CronTrigger(hour=1, minute=0)
        job = scheduler.add_job(run_command_at_1am, trigger=trigger, args=(job_name,))
        new_job = ScheduledJob(job_name=job_name, job_id=job.id)
        session.add(new_job)
        session.commit()
        return True
    return False


def run_command_at_1am(job_name):
    run_command(job_name)
    session = get_session()
    job_to_remove = session.query(ScheduledJob).filter_by(job_name=job_name).first()
    if job_to_remove:
        scheduler.remove_job(job_to_remove.job_id)
        session.delete(job_to_remove)
        session.commit()


async def schedule_command_endpoint(request: Request, command: str):
    username, password = await extract_credentials(request)

    if check_credentials(username, password):
        if schedule_command(command):
            return JSONResponse(
                content={"message": f"Command scheduled for 1 AM"}, status_code=200
            )
        else:
            return JSONResponse(
                content={"message": f"Command already scheduled for 1 AM"},
                status_code=400,
            )
    else:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)
