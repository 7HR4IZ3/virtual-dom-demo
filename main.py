from bottle import Bottle, static_file
from bottle_websocket import GeventWebSocketServer, websocket
from pages import *

HOST = "127.0.0.1"
PORT = 8080

app = Bottle()
app.install(websocket)

app.route("/_process_srv0", callback=dom.websocket)

@app.route("/static/<path:path>")
def _(path):
    return static_file(path, ".")

@app.route("/")
def index():
    return str(homepage)

@app.route("/clock")
def clock():
	return str(clockpage)

app.run(host=HOST, port=PORT, reloader=True, server=GeventWebSocketServer)
