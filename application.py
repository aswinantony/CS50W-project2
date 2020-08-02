import os

from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit

from login_decorator import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Keep track of channels created (Check for channel name)
channelsCreated = []

# Keep track of users logged (Check for username)
usersLogged = []

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/signin", methods=['GET','POST'])
def signin():
    ''' Save the username on a Flask session 
    after the user submit the sign in form '''

    # Forget any username
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        if len(username) < 1 or username is '':
            return render_template("error.html", message="username can't be empty.")

        if username in usersLogged:
            return render_template("error.html", message="that username already exists!")                   
        
        usersLogged.append(username)

        session['username'] = username

        # Remember the user session on a cookie if the browser is closed.
        session.permanent = True

        return redirect("/")

    else:
        return render_template("signin.html")

@app.route("/logout", methods=['GET'])
def logout():
    """ Logout user from list and delete cookie."""

    # Remove from list
    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass

    # exception ValueError is raised when an operation or function receives an argument that has the right type but an inappropriate value, 
    # and the situation is not described by a more precise exception such as IndexError.

    # Delete cookie
    session.clear()

    return redirect("/")

@app.route("/create", methods=['POST'])
def create():
    """ Create a channel and redirect to its page """

    # Get channel name from form
    newChannel = request.form.get("channel")

    if newChannel in channelsCreated:
        return render_template("error.html", message="that channel already exists!")

    # Add channel to global list of channels
    channelsCreated.append(newChannel)

@app.route("/channels/", methods=['GET','POST'])
@login_required
def enter_channel(channel):
    return render_template("channel.html")

