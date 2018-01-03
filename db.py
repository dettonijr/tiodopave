import json

DB_FILE = "botdb.json"
try:
    db = json.load(open(DB_FILE, "r"))
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
    json.dump(db, open(DB_FILE, "w"), ensure_ascii=False, indent=True)

def get_chats():
    global db
    chats = db["chats"]
    return chats
