import sys
sys.path.append("..")

from bottle import Bottle, static_file
from bottle_websocket import GeventWebSocketServer, websocket
from views import *

HOST = "127.0.0.1"
PORT = 8080

app = Bottle()
app.install(websocket)

app.route("/__process_svr0", callback=dom.websocket)

@app.route("/static/<path:path>")
def _(path):
    return static_file(path, "./assets")

@app.route("/")
def index():
    page = HomePage
    return page.render()

@app.route("/rooms/<name>")
def rooms(name):
	return RoomPage.render(name)

app.run(host=HOST, port=PORT, reloader=True, server=GeventWebSocketServer)
