"""Models for feedback app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def create_user(cls, user_details):
        hashed_pword = bcrypt.generate_password_hash(user_details['password'])
        hashed_utf8=hashed_pword.decode('utf8')
        user_details["password"]=hashed_utf8
        new_user = User(**user_details)
        return new_user

    @classmethod
    def authenicate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        return False



