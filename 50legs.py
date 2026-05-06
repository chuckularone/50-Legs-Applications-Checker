#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import datetime
import argparse
import os
import sys

# get arguments
parser = argparse.ArgumentParser(description="Read and print a file")
parser.add_argument("path", help="Directory path containing the file")
parser.add_argument("filename", help="Name of the file to read")
parser.add_argument("receiver_email", help="Name of the file to read")
parser.add_argument("passwordfile", help="Name of the file to read")
args = parser.parse_args()

# URL to scrape
# Read IP address from file and build the URL
with open("/home/chuck/code/python/scrape/ip.txt", "r") as f:
    ip_address = f.read().strip()
url = f"http://{ip_address}/chuck/temp.html"

target_text = "We are not currently accepting new applications."
email_fail_subject = "50 Legs not accepting applications"
email_success_subject = "APPLY TO 50 LEGS NOW!"
action_text = "APPLY NOW!"

# Create file paths
outFile = os.path.join(args.path, args.filename)
passFile = os.path.join(args.path, args.passwordfile)

# Read in the password for the sender
try:
    with open(passFile, "r") as f:
        password = f.read().strip()
except FileNotFoundError:
    print(f"Error: File not found: {passFile}", file=sys.stderr)
    sys.exit(1)
except PermissionError:
    print(f"Error: Permission denied: {passFile}", file=sys.stderr)
    sys.exit(1)

# Prepare email message
sender_email = "postmaster"
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = args.receiver_email

print()

try:
    # Request the URL
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    # Find the target text
    text_found = target_text in soup.get_text()
    #print(text_found)

    # Prepare result message
    if text_found:
        message["Subject"] =  email_fail_subject
        result_message = f"The text '{target_text}' was found on the website."
    else:
        message["Subject"] = email_success_subject
        result_message = f"The text '{target_text}' was NOT found on the website.\n" + action_text

    # Print result to screen
    print(result_message)

    # Write result to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(outFile, "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

except Exception as e:
    # Handle exceptions
    result_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
    print(result_message)

    # Write error to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(outFile, "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

# Attach result message with timestamp to email
timestamp_email = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message.attach(MIMEText(result_message, "plain"))

# Send email
with smtplib.SMTP_SSL("mail.theshanty.us", 465) as server:
    #server.set_debuglevel(2)
    server.login(sender_email, password)
    server.sendmail(sender_email, args.receiver_email, message.as_string())



