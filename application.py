import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channel")
def enter_channel():
    return render_template("channel.html")

# export FLASK_DEBUG=1
# export FLASK_APP=application.py