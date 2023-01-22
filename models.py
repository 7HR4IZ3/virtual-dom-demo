from sqlite import SqliteDatabase
from sqlite.columns import *

db = SqliteDatabase("db.sqlite3")

@db.on("error")
def error(e):
    raise e

@db.on("after_query")
def query(q, args, data):
    return
    print("Db Query:", q, "Args:", args, "Data:", data)

class User(db.Model):
    name: str

class Message(db.Model):
    sender: User
    value: str
    created: datetime
    seen_by: list[User]

class Room(db.Model):
    name: str
    messages: list[Message]
    created: datetime

    handlers = {}

    def send_message(self, user, message):
        Message.objects.create(sender=user, value=message, created=datetime.now(), seen_by=[])
        m = Message.objects.get().last()

        self.messages.append(m)
        self.save()

        self.trigger("message", m)
        return m
    
    def on(self, event, handler):
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]
    
    def trigger(self, event, *a, **kw):
        for handler in self.handlers.get(event, []):
            handler(*a, **kw)
