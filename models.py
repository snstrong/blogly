"""Models for Blogly."""

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
    # full_name = ''
    image_url = db.Column(db.String(), nullable=True)

    # def get_full_name(self):
    #     return f'{self.first_name} {self.last_name}'

    # def set_full_name(self, name):
    #     return self.full_name = name

    def __repr__(self):
        """Show info about pet."""
        i = self
        return f"<User {i.id} {i.full_name} {i.image_url}>"
