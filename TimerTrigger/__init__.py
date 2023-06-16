import feedparser
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import azure.functions as func

# Replace with your own mapping of email addresses to RSS feed URLs
EMAIL_RSS_MAP = {
    "email1@gmail.com": [
        "https://azurecomcdn.azureedge.net/en-us/blog/feed/",
        "https://cloudblogs.microsoft.com/microsoftsecure/feed/",
    ],
    "email2@gmail.com": [
        "http://www.veeam.com/blog/feed", 
        "https://cloudblogs.microsoft.com/microsoftsecure/feed/",
    ],
    # Add more emails and RSS feeds as needed
}

# OpenAI API URL for GPT-3
OPENAI_API_URL = "https://api.openai.com/v1/engines/text-davinci-002/completions"

# OpenAI API key
OPENAI_API_KEY = "----------------------------"

# Email settings
SMTP_SERVER = "localhost"
SMTP_PORT = 25
FROM_EMAIL = "testemail@ai.com"
EMAIL_PASSWORD = "Password123!"

def summarize(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }

    data = {
        'prompt': f'{text}\n\nIm IT specialist and need to understand will this article be interesting for me or not.Summarize next article. Summary should be 125 characters max and describe main idea of article.',
        'max_tokens': 150,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response_json = response.json()

    print(f"OpenAI response: {response_json}")  # Add this line

    if 'choices' in response_json and len(response_json['choices']) > 0:
        return response_json['choices'][0]['text'].strip()
    else:
        return None



def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # Comment out the following line to disable STARTTLS
    # server.starttls() # Secure the connection

    server.login(FROM_EMAIL, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(FROM_EMAIL, to_email, text)
    server.quit()

def main(mytimer: func.TimerRequest) -> None:
    for email, rss_feed_urls in EMAIL_RSS_MAP.items():
        email_body = ''

        for feed_url in rss_feed_urls:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                email_body += f'Title: {entry.title}\n'
                email_body += f'Link: {entry.link}\n'

                summary = summarize(entry.summary)
                if summary:
                    email_body += f'Summary: {summary}\n'
                else:
                    email_body += 'Could not generate a summary.\n'

                email_body += '-------------------------------\n'

        send_email(email, 'Your daily RSS summary', email_body)

if __name__ == "__main__":
    main(func.TimerRequest(""))
