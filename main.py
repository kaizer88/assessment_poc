from typing import Optional
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class Announcement(BaseModel):
    message: str
    scheduled_time: Optional[datetime] = None


# In-memory storage to keep track of sent announcements
sent_announcements = set()


# SQLite database for APScheduler
jobstore = {
    'default': SQLAlchemyJobStore(url='sqlite:///announcements.db')
}

# APScheduler configuration
executors = {
    'default': ThreadPoolExecutor(10),
}

scheduler = BackgroundScheduler(executors=executors, jobstores=jobstore)
scheduler.start()


def send_announcement(announcement: Announcement):
    current_time = datetime.now()

    if announcement.scheduled_time is None or announcement.scheduled_time <= current_time:
        # Send announcement immediately
        result = send_now(announcement)
        return {"message": f"{result['message']}"}
    else:
        # Schedule announcement for later
        scheduler.add_job(
            send_now,
            trigger=CronTrigger(year=announcement.scheduled_time.year, month=announcement.scheduled_time.month,
                                day=announcement.scheduled_time.day, hour=announcement.scheduled_time.hour,
                                minute=announcement.scheduled_time.minute),
            args=[announcement],
            id=str(announcement.scheduled_time)
        )
        return {"message": f"Announcement scheduled successfully"}


def send_now(announcement: Announcement):
    # Simulate sending the announcement
    if announcement.message not in sent_announcements:
        # In a real system, you would send the announcement via WhatsApp API
        # Record the sent announcement to avoid duplication
        sent_announcements.add(announcement.message)
        return {"message": f"Sending announcement: '{announcement.message}'"}
    else:
        # Duplicate announcement, raise an exception
        return {"message": f"Announcement '{announcement.message}' has already been sent."}


@app.get("/schedule-announcement", response_class=HTMLResponse)
async def schedule_announcement(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sending.html", context)


@app.post("/schedule-announcement", response_class=HTMLResponse)
async def schedule_announcement(request: Request, message: str = Form(...), scheduled_time: datetime = Form(None)):
    announcement = Announcement
    announcement.scheduled_time = scheduled_time
    announcement.message = message

    result = send_announcement(announcement)
    return templates.TemplateResponse("sending.html", context={"request": request, "message": [result["message"]]})

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8001)