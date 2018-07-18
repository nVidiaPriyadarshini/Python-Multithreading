from __future__ import absolute_import
import os
import redis
from celery import Celery
from celery.decorators import task
from celery.decorators import periodic_task
from celery.schedules import crontab
import time
from datetime import timedelta
from celery.result import AsyncResult
app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

@app.task(name='tasks.add')
def add(x, y):
    total = x + y
    print('{} + {} = {}'.format(x,y, total))
    return total

def backoff(attempts):
        """
	1, 2, 4, 8, 16,
	"""
	return 2 ** attempts

@app.task(bind=True, max_retries=4,soft_time_limit=5)
def data_extractor(self):
	try:
		for i in range(1, 11):
			print('Crawling HTML DOM!')
		        if i == 5:
				raise ValueError('Crawling index error')
	except Exception as exc:
		print('There was an exception, please retry after 5 seconds')
		raise self.retry(exc=exc, countdown=backoff(self.request.retries))

key = "4088587A2CAB44FD902D6D5C98CD2B17"

@periodic_task(bind=True,run_every=timedelta(seconds=3), name="_tasks.send_mail_from_queue")
def send_mail_from_queue(self):
        REDIS_CLIENT = redis.Redis()
	timeout = 60 * 5 # Lock expires in 5 mins"
	have_lock = False
	my_lock = REDIS_CLIENT.lock(key, timeout=timeout)

	try:
		have_lock = my_lock.acquire(blocking=False)
		if have_lock:
			message_sent= "example.email"
			print("{} Email message successfully sent, [{}]".format(self.request.hostname, message_sent))
     			time.sleep(10)
	finally:
		print("release resources")
		if have_lock:
			my_lock.release()

