import threading
import time
import random
import Queue

_queue = Queue.Queue(10)

class ProducerThread(threading.Thread):

	def run(self):
		numbers = range(5)
		global _queue
                while True:
			number = random.choice(numbers)
			_queue.put(number)
			print("Producer produced {}".format(number))
			time.sleep(1)

class ConsumerThread(threading.Thread):

	def run(self):
		global _queue
		while True:
			number = _queue.get()
                	_queue.task_done()
			print("Consumer consumed {}".format(number))
			time.sleep(1)

producer = ProducerThread()
producer.daemon = True
producer.start()

consumer = ConsumerThread()
consumer.daemon = True
consumer.start()

while True:
	time.sleep(1)
