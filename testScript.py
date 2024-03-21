#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import smtplib 
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import datetime

# URL to scrape
url = "https://50legs.org/application-for-assistance/"
curlcommand = "curl -X POST https://maker.ifttt.com/trigger/test_webhook/with/key/f4Lwi-yUBJL1cH1u0ocWrSrEaz9OFYBvBFrc5mtm0Jl"
# Senders and receivers
sender_email = "postmaster@theshanty.us"
receiver_email1 = "chuck@mckenna.tv"
#receiver_email2 = "cammckenna05@gmail.com"
password = "bTzRp2dN2*3#Qbnc"

# Prepare email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email1

try:
    # Request the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the target text
    target_text = "We are BLOOP not currently accepting new applications"
    text_found = target_text in soup.get_text()

    # Prepare result message
    if text_found:
        message["Subject"] = "50 Legs not accepting applications"
        result_message = f"The text '{target_text}' was found on the website."
    else:
        message.add_header('Importance', 'high')
        message.add_header('Priority', 'urgent')
        message["Subject"] = "APPLY TO 50 LEGS NOW!" 
        result_message = f"WOO HOO!!!!!\nThe text '{target_text}' was NOT FOUND on the website.\nAPPLY NOW!!"
        os.system(curlcommand)
    #
    # Print result to screen
    print(result_message)

    # Write result to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/chuck/code/python/scrape/out.txt", "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

except Exception as e:
    # Handle exceptions
    result_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
    print(result_message)

    # Write error to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/chuck/code/python/scrape/out.txt", "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

# Attach result message with timestamp to email
timestamp_email = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message.attach(MIMEText(f"{timestamp_email}: {result_message}", "plain"))

# Send email
with smtplib.SMTP_SSL("web179.dnchosting.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email1, message.as_string())
#    server.sendmail(sender_email, receiver_email2, message.as_string())


