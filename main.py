from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import os
from bot import init
import logging
import praw
import prawcore

REDDIT_ID = os.environ['REDDIT_ID']
REDDIT_SECRET = os.environ['REDDIT_SECRET']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def main():

    reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent="lol") 

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    init(reddit, updater)

if __name__ == '__main__':
    main()
