"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, DEFAULT_IMAGE_URL, Post

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
    """Redirect to users page"""

    return redirect("/users")

@app.get("/users")
def list_user():
    """List all user links"""

    users = User.query.all()
    # Improvement tip: make a query with an order by clause
    return render_template("user_listing.html",
                           users=users)

@app.get("/users/new")
def show_add_user_form():
    """Show create user form"""

    return render_template("user_form.html")

@app.post("/users/new")
def process_add_user_form():
    """Adding a new user to the database. Account for cases of no first or last
    name provided by redirecting to same page and flashing error message and
    account for no image url provided by giving it the default value we provide"""

    is_first_name_valid = True
    is_last_name_valid = True

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]


    first_name_trimmed = first_name.strip()
    last_name_trimmed = last_name.strip()
    image_url_trimmed = image_url.strip()


    if not first_name_trimmed:
        flash("You did not provide a first name")
        is_first_name_valid = False

    if not last_name_trimmed:
        is_last_name_valid = False
        flash("You did not provide a last name")

    if not is_first_name_valid or not is_last_name_valid:
        return redirect("/users/new")


    new_user = User(first_name=first_name,
                    last_name = last_name,
                    image_url = image_url_trimmed or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Shows the user detail page for the given id of the user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Shows the user edit form page"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.post("/users/<int:user_id>/edit")
def update_user_info(user_id):
    """Updates the user in the database"""

    is_first_name_valid = True
    is_last_name_valid = True

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    first_name_trimmed = first_name.strip()
    last_name_trimmed = last_name.strip()
    image_url_trimmed = image_url.strip()

    if not first_name_trimmed:
        flash("You did not provide a first name")
        is_first_name_valid = False

    if not last_name_trimmed:
        is_last_name_valid = False
        flash("You did not provide a last name")

    if not is_first_name_valid or not is_last_name_valid:
        return redirect(f"/users/{user_id}/edit")


    # retrieve user data from table
    user = User.query.get_or_404(user_id)

    user.first_name = first_name_trimmed
    user.last_name = last_name_trimmed

    user.image_url = image_url_trimmed or DEFAULT_IMAGE_URL

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

########### Post Routes ############

@app.get("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    """Displays form to add a post for that user"""

    user = User.query.get_or_404(user_id)

    return render_template("post_form.html",
                           user=user)

@app.post("/users/<int:user_id>/posts/new")
def process_add_post_form(user_id):
    """Add post and redirect to user detail page"""

    is_post_title_valid = True
    is_post_content_valid = True

    title = request.form["title"]
    content = request.form["content_field"]
    # TODO: Alternatively, can loop form fields and apply the same logic

    title_trimmed = title.strip()
    content_trimmed = content.strip()


    if not title_trimmed:
        flash("You did not provide a title")
        is_post_title_valid = False

    if not content_trimmed:
        is_post_content_valid = False
        flash("You did not provide any content")

    if not is_post_title_valid or not is_post_content_valid:
        return redirect("/users/<int:user_id>/posts/new")


    post = Post(title=title_trimmed,
                content=content_trimmed)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

