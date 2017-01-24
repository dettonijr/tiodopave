#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import logging
import praw
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
reddit = praw.Reddit(client_id="rRf-Ea8wPf4s0g", client_secret="7vsbdey9Uw0uyI1ErcsrrABtgiI", user_agent="lol") 

posts = list(reddit.subreddit("tiodopave").hot(limit=1000))
random.shuffle(posts)
print("STARTED")


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')

def piada(bot, update, args, job_queue, chat_data):
    global posts
    chat_id = update.message.chat_id
    try:
        n = posts[0]
        posts = posts[1:]
    except StopIteration:
        posts = reddit.subreddit("tiodopave").hot(limit=50)
        posts = list(reddit.subreddit("tiodopave").hot(limit=1000))
        random.shuffle(posts)
        n = posts[0]
        posts = posts[1:]
    try:
        due = int(args[0])
    except:
        due = 60

    sent_message = update.message.reply_text(n.title)
    def cb(bot, job):
        job.context.reply_text(n.selftext)
        #bot.sendMessage(job.context, text=n.selftext)
    job = Job(cb, due, repeat=False, context=sent_message)
    chat_data['job'] = job
    job_queue.put(job)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("320626558:AAEwncG_ehvNpw8xVLwW-V86cN_McZgdTUw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("piada", piada,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
