#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# URL to scrape
url = "https://50legs.org/application-for-assistance/"

# Senders and receivers
sender_email = "postmaster@theshanty.us"
receiver_email = "chuck@mckenna.tv"
password = "bTzRp2dN2*3#Qbnc"

# Prepare email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Script Execution Status"

try:
    # Request the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the target text
    target_text = "We BLOOP are not currently accepting new applications"
    text_found = target_text in soup.get_text()

    # Prepare result message
    if text_found:
        result_message = f"The text '{target_text}' was found on the website."
        # Execute curl command
        os.system("curl -X POST https://maker.ifttt.com/trigger/50Legs/with/key/f4Lwi-yUBJL1cH1u0ocWrSrEaz9OFYBvBFrc5mtm0Jl -o output_file.txt")
    else:
        result_message = f"The text '{target_text}' was not found on the website."

    # Print result to screen
    print(result_message)

except Exception as e:
    # Handle exceptions
    result_message = f"An error occurred: {str(e)}"
    print(result_message)

# Attach result message to email
message.attach(MIMEText(result_message, "plain"))

# Send email
with smtplib.SMTP_SSL("web179.dnchosting.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())


