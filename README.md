#  Proof of Concept

**Table of Contents**
1. [Proposal of at least 2 reasons](#Course-of-the-Problem), Proposal of at least 2 reasons.
2. [Proposal of an architecture](#Proposal-of-an-architecture), Proposal of an architecture.
3. [Application setup](#Application-setup), Application setup steps.


## Course of the Problem.

* Concurrency Issues: If multiple instances of the cron job or announcement-sending process run concurrently, there might be a race condition. Two instances might pick up the same announcement to send simultaneously, leading to duplicates.

* Notification Failures: In scenarios where the announcement sending involves interacting with external services (e.g., WhatsApp API), a failure in acknowledgment or confirmation might lead the system to attempt resending the announcement.


## Proposal of an architecture.

* Database Locking Mechanism: Introduce a database locking mechanism to ensure that only one instance of the cron job or announcement-sending process can access and process announcements at any given time. This prevents concurrent instances from duplicating the sending process.

* Tracking Sent Announcements: Maintain a record of sent announcements in the database, including a timestamp. Before sending any announcement, check the database to ensure that a similar announcement hasn't been sent within a certain timeframe. This helps avoid duplicate sends.

* Asynchronous Processing: Use a message queue system to handle the announcement sending asynchronously. The cron job adds announcements to the queue, and worker processes pull and process them. This ensures sequential processing and avoids concurrent duplication.

## Application setup.



* **⚠️ Please read these instructions.**

* Clone this repo on your machine.
* Run the command to install requirements
```
pip install - r requirements
```
* Run the command to run tests
```
pytest test_tasks.py
```
* Run the command to run the app
```
python main.py
```
* Go to link to write an message
```
http://127.0.0.1:8001/schedule-announcement
```

* This app allows a user to send messegaes and store them in memoey in a set().
* You can schedute them buy selecting the datetime and is optional datetime, however you are required to type a message.
* You can only send a duplicates if you are scheduling the message however it will not be sent.




