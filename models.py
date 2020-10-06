"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Blogly User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(15),
                    nullable=False,
                    unique=False)
    last_name = db.Column(db.String(15),
                    nullable=False,
                    unique=False)
    # TODO: DEFAULT IMG URL NOT WORKING??? NEED TO FIX
    image_url = db.Column(db.String(),
                    nullable=False,
                    default="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
    posts = db.relationship("Post",
                    backref="user",
                    cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""
        i = self
        return f"<User {i.id} {i.full_name} {i.image_url}>"

class Post(db.Model):
    """Blog post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(15),
                    nullable=False,
                    unique=False)
    content = db.Column(db.String(),
                    nullable=False,
                    unique=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'),
                    nullable=False)
    
    def __repr__(self):
        """Show info about post."""
        i = self
        return f"<Post {i.id} {i.created_at} {i.title} {i.content}>"
