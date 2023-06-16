RSS Summary Email Sender

This application parses provided RSS feeds, summarizes the feed entries using OpenAI's language model, and then sends an email summary of the feeds to specified email addresses.

Prerequisites

Python 3.6 or later
An OpenAI account and API key
RSS feeds you want to parse
An SMTP server for sending emails

Installation
Clone this repository to your local machine.
Install the required Python packages:
bash
Copy code
pip install feedparser requests azure-functions

Configuration
Before running the script, you need to configure the following parameters in the script:

EMAIL_RSS_MAP: a Python dictionary mapping email addresses to a list of RSS feed URLs. The script will send an email to each address with a summary of the corresponding RSS feeds.
OPENAI_API_URL: the API URL for the OpenAI language model. 
OPENAI_API_KEY: your OpenAI API key, which you can find in your OpenAI account dashboard.
SMTP_SERVER: the hostname or IP address of your SMTP server.
SMTP_PORT: the port your SMTP server is running on.
FROM_EMAIL: the email address that the summary emails should be sent from.
EMAIL_PASSWORD: the password for the FROM_EMAIL account.

Usage
You can run the script manually with:

bash
Copy code
python main.py
The script can also be triggered by an Azure Timer function if deployed in an Azure Function App. It currently triggers whenever the Timer function is called, but you could configure the Timer function to call the script at regular intervals (e.g., daily).

The script will parse the RSS feeds, generate a summary for each feed entry, and send an email to each address in EMAIL_RSS_MAP with the summaries.

Support
For any issues, questions, or concerns, please open an issue on this repository.

Disclaimer
This script uses OpenAI's language model, which has a usage quota. If you exceed your quota, you will need to wait until it resets or upgrade your OpenAI plan. The script does not currently handle quota errors gracefully; it will simply fail with an error message from the OpenAI API.