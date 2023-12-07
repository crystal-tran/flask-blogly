"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    image_url = db.Column(
        db.Text(),
        default='/static/img/default_profile_image.jpg'
    )


def connect_db(app):
    """Connect the database to our Flask app."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

