from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import sys

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_database_uri():
    if "python3 -m unittest" in sys.argv:
        return 'postgresql:///flask_feedback_test'
    return 'postgresql:///flask_feedback'

def get_echo_TorF():
    if "python3 -m unittest" in sys.argv:
        return False
    return True


class User(db.Model):
    """User"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), primary_key=True, unique = True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref="user", cascade="all, delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with a hashed password and return user object"""

        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into normal (unicode uft-8) string
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password = hashed_utf8, email = email, first_name = first_name, last_name = last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Return user if credentials are valid, else return false"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
class Feedback(db.Model):
    """User Feedback"""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable=False)
    content= db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)
    # title content username