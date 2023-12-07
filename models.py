"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = 'https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg'
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
        default= DEFAULT_IMAGE_URL
    )


def connect_db(app):
    """Connect the database to our Flask app."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

