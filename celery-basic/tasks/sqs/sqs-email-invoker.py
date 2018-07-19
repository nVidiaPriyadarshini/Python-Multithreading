import boto3
import json
from uuid import uuid4
import  uuid
from .config import QUEUE_URL, ACCESS_KEY, SECRET_KEY

sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def send_sample_email():
 	#Create body of email
	text= "Hello from Vidya"
	html= """\
	<html>
	<head></head>
	<body>
	<p>Hi!<br>
	How are you?<br>
	Here is a reference <a href = "http://www.google.com">link</a>
	</p>
	</body>
	</html>
	"""
        
	to_email = "svppueds@sharklasers.com"
	subject = "<subject>"
        cc_email = ['nVidiaPriyadarshini@gmail.com']
	bcc_email = ['test@gmail.com']

	body = json.dumps({'jobId': str(uuid.uuid4()), 'to_email': to_email, 'subject': subject, 'data': { 'text': text , 'html': html }, 'cc_email': cc_email, 'bcc_email': bcc_email })

	response = sqs.send_message(
			QueueUrl= QUEUE_URL,
			MessageBody=body
			)

	print(response)	
	print("SUCCESS")

send_sample_email()
