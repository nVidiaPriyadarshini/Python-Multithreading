from __future__ import absolute_import
import os
from celery import Celery
from celery.decorators import task
from celery.decorators import periodic_task
from celery.schedule import crontab
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

@periodic_task(run_every=timedelta(seconds=3), name="_tasks.send_mail_from_queue")
def send_mail_from_queue():
	try:
		message_sent= "example.email"
		print("Email message successfully sent, [{}]".format(message_sent))
	finally:
		print("release resources")


