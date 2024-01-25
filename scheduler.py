from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from pytz import utc
from update_data import update_data

app = Flask(__name__)
scheduler = BackgroundScheduler(timezone=utc)

scheduler.add_job(update_data, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    return "Welcome to the Football Data Update Service!"

if __name__ == '__main__':
    try:
        app.run()
    finally:
        scheduler.shutdown()