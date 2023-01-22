from virtual_dom import VirtualDom, BaseContext, Reactive, task, JsObject, LocalStorage, Page, SessionStorage, HTML
from bottle import jinja2_template as render
from random import randint

from models import User, Message, Room, List, datetime

dom = VirtualDom()
h = HTML()

class Rooms:
    def create(self, name) -> Room:
        room = Room(name=name, created=datetime.now(), messages=[])
        room.save()
        return room

    def delete(self, room_id):
        Room.objects.delete(id=room_id)
    
    def get(self, room_id) -> Room:
        return Room.objects.get_one(id=room_id)
    
    @property
    def all(self) -> List[Room]:
        return Room.objects.all()

rooms = Rooms()

class BasePage(Page):
    def html(self, body, extra_head=[], extra_body=[], head_attrs={}, body_attrs={}):
        htm = self.HTML
        return htm.html(
            htm.head(
                htm.link(),
                *extra_head,
                **head_attrs
            ),
            htm.body(
                body,
                *extra_body,
                **body_attrs
            )
        )

@dom.register
class HomePage(Page):
    username = SessionStorage()
    interval = None

    new_messages = []
    clients = []

    @property
    def user(self):
        return User.objects.get_one(name=self.username)

    def get_new_messages(self, user, room_id):
        new  = []
        room = rooms.get(int(room_id))
        for message in room.messages:
            if not list(filter(lambda u: u.id == user.id, message.seen_by)):
                new.append(message)
                message.seen_by.append(user)
                message.save()
        # print(user, new)
        return new

    def create_room(self):
        input = self.browser.document.querySelector('input[name="room_name"]').eval()
        if input.value:
            room = rooms.create(input.value)

            doc = self.browser.document.eval()

            rooms_section = doc.querySelector("#rooms_list")
            rooms_section.innerHTML += render("_room_details.html", {"room": room})
        else:
            self.browser.alert("Invalid name. ")

    def set_username(self):
        input = self.browser.document.querySelector('input[name="user_name"]').eval()
        if input.value:
            self.username = input.value

            if not self.user:
                User.objects.create(name=self.username)
        else:
            self.browser.alert("Invalid username.")
    
    def set_room(self, room_id):
        room = rooms.get(int(room_id))
        if room:
            self.room = room
            # self.room.on("message", )

            self.browser.document.querySelector("#chat_view #chat_details").js("?").remove().eval()

            chat_view = self.browser.document.querySelector("#chat_view").eval()
            tpl = render("_room.html",  {"room": room, "user": self.user})
            chat_view.innerHTML += tpl

            if self.interval:
                self.browser.clearInterval(self.interval)
            self.interval = self.browser.setInterval(lambda: self.check_message(room_id), 500).eval()
        else:
            self.browser.alert("No such room.")

    def send_message(self, room_id):
        room = rooms.get(int(room_id))
        if room:
            input = self.browser.document.querySelector('input[name="message_text"]').eval()
            if input.value:
                room.send_message(self.user, input.value)
                input.value = ""
        else:
            self.browser.alert("No such room.")

    def check_message(self, room_id):
        user = self.user
        tpl = [
            render("_room_message.html",  {"message": message, "user": user}) for message in self.get_new_messages(user, room_id)
        ]
        if tpl:
            html = self.browser.document.querySelector("#chat-messages").innerHTML.eval()
            self.browser.document.querySelector("#chat-messages").innerHTML = html + ("".join(tpl))

    def on_client_connected(self, *args):
        if not self.username:
            self.username = self.browser.prompt("Enter username:")
        self.browser.document.querySelector('input[name="user_name"]').setAttribute("value", self.username)
    
    def on_client_disconnected(self, *args):
        if self.interval:
            pass
            # self.browser.clearIterval(self.interval)
    
    def on_client_message(self, *args):
        self.browser.alert("New message")

    def html(self):
        return render("index.html", {"rooms": rooms.all})


@dom.register
class RoomPage(Page):
    def html(self):
        h = self.HTML
        return h.main(
            h.div(
                id="chats"
            ),
            h.section(
                h.input(placeholder="Enter Message")
            )
        )
