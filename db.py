import pickle

DB_FILE = "bot.db"
try:
    db = pickle.load(open(DB_FILE, "rb"))
except FileNotFoundError:
    db = {"chats": {}}

def is_chat(chat_id):
    global db
    chats = db["chats"]
    return chat_id in chats.keys()

def add_chat(chat_id, name):
    global db
    chats = db["chats"]
    chats[chat_id] = {"name":name}
    pickle.dump(db, open(DB_FILE, "wb"))

def get_chats():
    global db
    chats = db["chats"]
    return chats
