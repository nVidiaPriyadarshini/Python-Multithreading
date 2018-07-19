import traceback
import smtplib
import boto3
import json
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import QUEUE_URL, ACCESS_KEY, SECRET_KEY
sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

gmail_user = "nVidiaPriyadarshini@gmail.com"
gmail_pwd = "test1234!"
 
def send_mail(to, subject, text, html, **kwargs):
	msg = MIMEMultipart('alternative')
	msg['From'] = gmail_user
	msg['To'] = to
	if kwargs.get('cc', None):
		msg['Cc'] = ','.join(kwargs.get('cc'))
	if kwargs.get('bcc', None):
		msg['Bcc'] = ','.join(kwargs.get('bcc'))
	msg['Subject'] = subject

	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
		
	msg.attach(part1)
	msg.attach(part2)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()	

	mailServer.login(gmail_user, gmail_pwd)

	mailServer.sendmail(gmail_user, to, msg.as_string())

	mailServer.close()


if __name__ == '__main__':
        print('Starting worker listening on {}'.format(QUEUE_URL))
        while True:
                response = sqs.receive_message(QueueUrl=QUEUE_URL,
                                               AttributeNames=['All'],
                                               MessageAttributeNames=['string',],
                                               MaxNumberOfMessages=1,
                                               WaitTimeSeconds=10,
                )
                messages = response.get('Messages', [])
                for message in messages:
                     try:
                       print('Message Body > ', message.get('Body'))
                       body = json.loads(message.get('Body'))
                       if not body.get('jobId', None):
                        print('JobId not provided!')
                       	sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message.get('ReceiptHandle'))
                        print('Received and deleted message: {}'.format(message))
                       else:
                        job_id = body.get('jobId')
                        print('Running Job Id {}'.format(job_id))
			send_mail(body.get('to_email'),body.get('subject'),body.get('data').get('text'),body.get('data').get('html'), **{'cc': , body.get('cc_email'), 'bcc': , body.get('bcc_email')})
                        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message.get('ReceiptHandle'))
                        print('Received and deleted message: {}'.format(message))
                       except Exception as e:
                                print('Exception in worker > ', e)
                                #sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message.get('ReceiptHandle'))
        time.sleep(10)

print('WORKER STOPPED')
