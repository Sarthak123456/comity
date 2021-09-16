import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
django.setup()


from apscheduler.schedulers.blocking import BlockingScheduler
#IMPORTANT! Have to make sure things are working before this starts
from django import setup
setup()

sched = BlockingScheduler()

@sched.scheduled_job('interval', days=1)
def timed_job():
    print('hello')
    return