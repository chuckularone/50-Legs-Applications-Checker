#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
import datetime

# URL to scrape
url = "https://50legs.org/application-for-assistance/"

# Senders and receivers
sender_email = "makerandfixerofthings@gmail.com"
receiver_email = "chuck@mckenna.tv"
password = "F5o71f!3DLCRdCnMGp42LltW3a5Qk35s$UU#"

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
    target_text = "We are not currently accepting new applications"
    text_found = target_text in soup.get_text()

    # Prepare result message
    if text_found:
        result_message = f"The text '{target_text}' was found on the website."
    else:
        result_message = f"The text '{target_text}' was not found on the website."

    # Print result to screen
    print(result_message)

    # Write result to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("out.txt", "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

except Exception as e:
    # Handle exceptions
    result_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
    print(result_message)

    # Write error to file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("out.txt", "a") as file:
        file.write(f"{timestamp}: {result_message}\n")

# Attach result message with timestamp to email
timestamp_email = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message.attach(MIMEText(f"{timestamp_email}: {result_message}", "plain"))

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

