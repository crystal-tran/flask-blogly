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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



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

    image_url_trimmed = image_url.strip()
    #if we retrieve a url, set image_url to that url
    #if we retrieve an empty string, set that value to None

    if not image_url_trimmed:
        image_url_trimmed = None

    new_user = User(first_name=first_name,
                    last_name = last_name,
                    image_url = image_url_trimmed)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("user_edit.html", user=user)

@app.post("/users/<int:user_id>/edit")
def save_button(user_id):
    """Updates the user in the database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    # retrieve user data from table
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes the user"""
    user = User.query.get_or_404(user_id)
    print("user is:", user)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# INSERT INTO users(first_name, last_name)
#     VALUES('Crystal', 'Tran')