from app import db, app
from models import User

app.app_context().push()

db.drop_all()
db.create_all()

user = User.register(
    username = "Barksley123",
    pwd = "woofwoof",
    email = "barks.ley@email.com",
    first_name = "Barksley",
    last_name = "Woofinton"
)

db.session.add(user)
db.session.commit()