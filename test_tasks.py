from datetime import datetime, timedelta
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from main import Announcement, send_announcement, send_now

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


def test_now_announcement():
    announcement_data = {
        "message": "Test announcement now 1",
        "scheduled_time": datetime.now()
    }
    announcement = Announcement
    announcement.scheduled_time = announcement_data["scheduled_time"]
    announcement.message = announcement_data["message"]
    response = send_announcement(announcement)
    assert response == {"message": f"Sending announcement: '{announcement.message}'"}


def test_schedule_announcement():
    announcement_data = {
        "message": "Test announcement scheduled",
        "scheduled_time": datetime.now() + timedelta(minutes=5)
    }
    announcement = Announcement
    announcement.scheduled_time = announcement_data["scheduled_time"]
    announcement.message = announcement_data["message"]
    response = send_announcement(announcement)
    assert response == {"message": "Announcement scheduled successfully"}


def test_send_announcement():
    announcement_data = {
        "message": "Test announcement 123",
        "scheduled_time": datetime.now()
    }
    announcement = Announcement
    announcement.scheduled_time = announcement_data["scheduled_time"]
    announcement.message = announcement_data["message"]
    response = send_now(announcement)
    assert response["message"] == f"Sending announcement: '{announcement.message}'"


def test_check_duplicate_announcement():
    announcement_data = {
        "message": "Test announcements",
        "scheduled_time": datetime.now()
    }
    announcement = Announcement
    announcement.scheduled_time = announcement_data["scheduled_time"]
    announcement.message = announcement_data["message"]
    send_now(announcement)
    response = send_now(announcement)
    assert response["message"] == f"Announcement '{announcement.message}' has already been sent."
