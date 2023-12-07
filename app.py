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

    users = User.query.all()
    return render_template("user_listing.html",
                           users=users)

@app.get("/users/new")
def show_add_user_form():
    """Listen for add user button"""

    return render_template("user_form.html")

@app.post("/users/new")
def process_add_user_form():
    """Adding a new user to the database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                     last_name = last_name,
                     image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


# INSERT INTO users(first_name, last_name)
#     VALUES('Crystal', 'Tran')