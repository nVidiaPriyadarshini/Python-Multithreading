from __future__ import absolute_import
import os
from celery import Celery
from celery.decorators import task
app = Celery('tasks', backend=None, broker='redis://localhost:6379/0')

@app.task(name='tasks.add')
def add(x, y):
    print('{} + {} = {}'.format(x,y, x + y))

add.delay(7, 8)
