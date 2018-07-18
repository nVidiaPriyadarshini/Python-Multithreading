import boto3
import time

from .config import DLQ_URL, ACCESS_KEY, SECRET_KEY
sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

if __name__ == '__main__':
	print('Starting worker listening on {}'.format(DLQ_URL))
	while True:
		response = sqs.receive_message(QueueUrl=DLQ_URL,
					       AttributeNames=['All'],
					       MessageAttributeNames=['string',],
					       MaxNumberOfMessages=1,
					       WaitTimeSeconds=10,
		)
		messages = response.get('Messages', [])
		for message in messages:
				print('Message Body > ', message.get('Body'))
				sqs.delete_message(QueueUrl=DLQ_URL, ReceiptHandle=message.get('ReceiptHandle'))

	time.sleep(10)
print('WORKER STOPPED')
