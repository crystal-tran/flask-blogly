"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "blogly"

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.get("/")
def redirect_to_users():
    """Lists users"""

    return redirect("/users")

@app.get("/users")
def list_user():
    """List all user links"""

    # users = User.query.all()
    # return render_template("userListing.html",
    #                        users=users)

@app.get("/users/new")
def show_add_user_form():
    """Listen for add user button"""

    return render_template("user_form.html")




# INSERT INTO users(first_name, last_name)
#     VALUES('Crystal', 'Tran')