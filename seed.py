from app import db, app
from models import User, Feedback

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

    # title content username

post1 = Feedback(
    title = "Wow feedback!",
    content = "Lorem ipsum and all that, blah blah blah",
    username = "Barksley123"
)
post2 = Feedback(
    title = "THIS IS A TITLE!",
    content = "Why is the title all in caps? Because I'm excited of course! Who wouldn't be! What a time to be alive",
    username = "Barksley123"
)
post3 = Feedback(
    title = "Bark",
    content = "Grrr WOOF WOOF rrrrghgrr BARK huff grrrrowl snort BARK",
    username = "Barksley123"
)

db.session.add_all([post1, post2, post3])
db.session.commit()