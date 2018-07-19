import boto3
import json

from .config import QUEUE_URL, ACCESS_KEY, SECRET_KEY

sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def send_report_results():

	payload = json.dumps({'jobId': 'test01', 'data': { 'topping': [
			{'id': '5001', 'type': 'Chery'},
			{'id': '5002', 'type': 'Glazed'},
			{'id': '5003', 'type': 'Sugar'},
			{'id': '5004', 'type': 'Powdered Sugar'},
			{'id': '5007', 'type': 'Choclate with Sprinkles'},
			{'id': '5010', 'type': 'Choclate'},
			{'id': '5006', 'type': 'Maple'}]
		}}) 

	response = sqs.send_message(
			QueueUrl= QUEUE_URL,
			MessageBody="This will cause Exception"
			)

	print(response)	
	print("SUCCESS")

send_report_results()
