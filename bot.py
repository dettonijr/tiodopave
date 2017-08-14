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
import prawcore
import random
import urllib
import urllib.request
import json
import os

REDDIT_ID = os.environ['REDDIT_ID']
REDDIT_SECRET = os.environ['REDDIT_SECRET']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent="lol") 

posts = list(reddit.subreddit("tiodopave").hot(limit=200))
random.shuffle(posts)
jokeposts = list(reddit.subreddit("DadJokes").hot(limit=200))
random.shuffle(jokeposts)

brasilposts = list(reddit.subreddit("brasil").hot(limit=50))
random.shuffle(brasilposts)

status_phrases = [
"tá o bagaço.",
"tá pela capa da gaita.",
"tá só o legume desidratado do Cup Noodles.",
"tá só o caldinho do miojo"
"tá só a embalagem individual da fatia do Sandwich-In.",
"tá so o lacre do polenguinho",
"ta só a chapa do grill",
"tá só o rabo do ornitorrinco.",
"ta so o topete da cacatua",
"tá só o saco da bisnaguinha.",
"tá só a beirada do pão Pulmann",
"tá só a régua Desetek.",
"tá só o bastão de cola quente",
"tá só a listra do pijama do B1 e do B2.",
"ta so a bolsa do tinky winky",
"tá só o cipó do Tarzan.",
"tá só o couro da jaguatirica",
"tá só o macaco do Latino.",
"tá só a boina da Kelly Key",
"tá só a polpa do abacate.",
"tá só o caroço da siriguela",
"tá só a casca do inhame.",
"tá só o fiapo da mandioca",
"tá só a farinha de rosca.",
"ta so o farelo da broa",
"tá só a canetinha estourada.",
"tá só a tampinha da tinta guache",
"tá só o selo do Yakult.",
"tá só o Clight de limão.",
"ta só o tang de maracujá",
"tá só o sapato do papa Francisco.",
"tá só o fusca do mujica",
"tá só a peruca do Valderrama.",
"ta só o bigodinho do vampeta",
"ta só o cadaro do kichute",
"tá só o capacete do Robocop.",
"tá só a bota do rambo",
"tá só o cartucho genérico da HP.",
"ta so o mouse da maxprint",
"tá só o bonsai de romã.",
"tá só o galho da goiabeira",
"tá só o copinho do exame de urina.",
"ta só a chapa do raio x",
"tá só o topete do Cabeção da Malhação.",
"ta so a pinta do eri johnson",
"tá só o Chamyto.",
"tá só o mupy de pessego",
"tá só a pelúcia pirata do Pikachu.",
"tá só o digimon com tosse",
"tá só o maço do Gudang Garam.",
"tá só a chepa do Gudang Garam.",
"tá só o Schumacher de GoPro.",
"ta só o selo do derby vermelho",
"tá só o molho agridoce do rolinho primavera.",
"tá só a couve-flor do yakisoba",
"tá só a tripa do salame.",
"tá só o barbante da linguiça",
]


print("STARTED")


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Olá! Digite /piada para receber uma piada especial do Tio do Pavê')


def help(bot, update):
    update.message.reply_text('Precisa de ajuda? É simples! Digite /piada para receber uma piada especial do Tio do Pavê')

def status(bot, update, args, job_queue, chat_data):
    global posts
    chat_id = update.message.chat_id
    name = " ".join(args)
    if name == "":
       name = update.message.from_user.first_name

    phrase = random.choice(status_phrases)
    name = name.replace("não","").replace("nao","")
    if "proxeneta" in name.lower() or name == "@iucas" or "luk" in name.lower() or "luc" in name.lower():
        phrase = random.choice([
            "ta só o pão com mortadela do MST.",
            "ta só o mindinho do Lula",
            "ta só o boné da CUT",
            "ta só o triplex do Lula",
            "ta só o funcionário do sindicato",
            "ta só o concursado da UFSC",
            "ta só a Dilma Roussef",
            "ta só a barba do Fidel Castro",
            "ta só a boina do Che Guevara"
        ])

    bot.send_message(chat_id=chat_id, text = "%s %s" % (name, phrase))

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
        due = 30

    sent_message = update.message.reply_text(n.title)
    def cb(bot, job):
        job.context.reply_text(n.selftext)
        #bot.sendMessage(job.context, text=n.selftext)
    job = Job(cb, due, repeat=False, context=sent_message)
    chat_data['job'] = job
    job_queue.put(job)

def joke(bot, update, args, job_queue, chat_data):
    global jokeposts
    chat_id = update.message.chat_id
    try:
        n = jokeposts[0]
        jokeposts = jokeposts[1:]
    except StopIteration:
        jokeposts = list(reddit.subreddit("DadJokes").hot(limit=1000))
        random.shuffle(jokeposts)
        n = jokeposts[0]
        posts = jokeposts[1:]
    try:
        due = int(args[0])
    except:
        due = 30

    sent_message = update.message.reply_text(n.title)
    def cb(bot, job):
        job.context.reply_text(n.selftext)
        #bot.sendMessage(job.context, text=n.selftext)
    job = Job(cb, due, repeat=False, context=sent_message)
    chat_data['job'] = job
    job_queue.put(job)

def politica(bot, update, args, job_queue, chat_data):
    global brasilposts
    try:
        n = brasilposts[0]
        brasilposts = brasilposts[1:]
    except StopIteration:
        brasilposts = list(reddit.subreddit("brasil").hot(limit=100))
        random.shuffle(brasilposts)
        n = brasilposts[0]
        posts = brasilposts[1:]

    print (n)
    update.message.reply_text("Titulo: %s\n\nTexto:%s\n\nURL: %s" % (n.title, n.selftext, n.shortlink))

def top(bot, update, args, job_queue, chat_data):
    if len(args) == 0:
        return None
    try:
        posts = list(reddit.subreddit(args[0]).hot(limit=1))
    except prawcore.exceptions.NotFound:
        update.message.reply_text("Not found")
        return None
    except Exception as error:
        update.message.reply_text("Unknown error %s" % str(error))
        return None
    
    if len(posts) == 0:
        return None
    n = posts[0]
    text = n.selftext
    if len(text) > 500:
        text = text[:500] + " [...]"

    update.message.reply_text("Titulo: %s\n\nTexto:%s\n\nURL: %s" % (n.title, text, n.shortlink))

def new(bot, update, args, job_queue, chat_data):
    if len(args) == 0:
        return None
    try:
        posts = list(reddit.subreddit(args[0]).new(limit=1))
    except prawcore.exceptions.NotFound:
        update.message.reply_text("Not found")
        return None
    except Exception as error:
        update.message.reply_text("Unknown error %s" % str(error))
        return None
    
    if len(posts) == 0:
        return None
    n = posts[0]
    text = n.selftext
    if len(text) > 500:
        text = text[:500] + " [...]"

    update.message.reply_text("Titulo: %s\n\nTexto:%s\n\nURL: %s" % (n.title, text, n.shortlink))

def defina(bot, update, args, job_queue, chat_data):
    if len(args) == 0:
        return None
    palavra = args[0]    
    try:
        f = urllib.request.urlopen("http://dicionario-aberto.net/search-json/" + urllib.parse.quote(palavra))
        j = json.loads(str(f.read(), "utf-8"))        
    except urllib.error.HTTPError as error:
        if error.code == 404:
            update.message.reply_text("Not found")
        else:
            update.message.reply_text("Error %d" % error.code)
        return None
    except Exception as error:
        update.message.reply_text("Unknown error %s" % str(error))
        return None
    items = j['entry']['sense']
    if len(items) > 1:
        update.message.reply_text(
          "\n".join(["%d) %s" % (i + 1, x['def']) for i, x in enumerate(items)])
        )
    else:
        update.message.reply_text(items[0]['def'])

def randomm(bot, update, args, job_queue, chat_data):
    if len(args) == 0:
        return None
    try:
        posts = reddit.subreddit(args[0]).random()
    except prawcore.exceptions.NotFound:
        update.message.reply_text("Not found")
        return None
    except Exception as error:
        update.message.reply_text("Unknown error %s" % str(error))
        return None
    
    n = posts
    text = n.selftext
    if len(text) > 500:
        text = text[:500] + " [...]"

    update.message.reply_text("Titulo: %s\n\nTexto:%s\n\nURL: %s" % (n.title, text, n.shortlink))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("piada", piada,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))

    dp.add_handler(CommandHandler("joke", joke,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))

    dp.add_handler(CommandHandler("status", status,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))
    dp.add_handler(CommandHandler("politica", politica,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))
    dp.add_handler(CommandHandler("top", top,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))
    dp.add_handler(CommandHandler("random", randomm,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))
    dp.add_handler(CommandHandler("new", new,
                                  pass_args=True,
            	                pass_job_queue=True,
                                pass_chat_data=True))
    dp.add_handler(CommandHandler("defina", defina,
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
