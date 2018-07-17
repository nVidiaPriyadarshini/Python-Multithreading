import threading
import time
import random

queue = []
MAX_ITEMS = 10

condition = threading.Condition()

class ProducerThread(threading.Thread):

	def run(self):
		numbers = range(5)
		global queue

		while True:
			condition.acquire()
			if len(queue) == MAX_ITEMS:
				print("Queue is full, producer is waiting")
				condition.wait()
				print("Space in queue, Consumer notified Producer")
			number = random.choice(numbers)
			queue.append(number)
			print("Producer produced {}".format(number))
			condition.notify()
			condition.release()
			time.sleep(random.random())

class ConsumerThread(threading.Thread):

	def run(self):
		global queue
		while True:
			condition.acquire()
			if len(queue) == 0:
				print("Queue is empty, consumer is waiting")
				condition.wait()
				print("Producer adding something to queue")
			number = queue.pop(0)
			print("Consumer consumed {}".format(number))
			condition.notify()
			condition.release()
			time.sleep(random.random())

producer = ProducerThread()
producer.start()

consumer = ConsumerThread()
consumer.start()
