import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

'''
POST
Header - application/json
Body - purpose, recipient email, name, email body
'''

def send_email(event, context):		# event contains request data, context contains other runtime data
	# Recieve data
	body = json.loads(event['body'])
	print(body)
	purpose = body['purpose']
	recipient_email = body['recipient_email']
	recipient_name = body['recipient_name']
	email_body = body['email_body']

	# Email Configuration
	smtp_server = "smtp.gmail.com"
	smtp_port = 587
	email_id = os.getenv("EMAIL_ID")
	password = os.getenv("GMAIL_APP_PASS")
	
	try:
		if purpose == "signup":
			subject = "Welcome to the team"
		else:
			subject = "You have a new booking"
			
		msg = MIMEMultipart()
		msg['From'] = email_id
		msg['To'] = recipient_email
		msg['Subject'] = subject

		msg.attach(MIMEText(email_body, 'plain'))

		with smtplib.SMTP(smtp_server, smtp_port) as server:
		    server.starttls()
		    server.login(email_id, password)
		    server.sendmail(email_id, recipient_email, msg.as_string())
		    
		response = {"statusCode": 200, "body": json.dumps({"status":"Message sent successfully"})}

	except Exception as e:
		print(f"Error sending email: {e}")
		response = {"statusCode": 404, "body": json.dumps({"status":"Something went wrong"})}
		
	return response
