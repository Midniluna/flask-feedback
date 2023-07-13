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

user2 = User.register(
    username = "4N0N",
    pwd = "sosecretwowo",
    email = "anon.ymous@email.com",
    first_name = "Mystery",
    last_name = "Mann"
)



db.session.add_all([user, user2])
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


post4 = Feedback(
    title = "Title title",
    content = "There is content to be had here. Too bad it's secret, only I can see this!",
    username = "4N0N"
)
post5 = Feedback(
    title = "I am not a ninja",
    content = "Believe me you'd know a ninja if you saw one. Surely. Oh this katana? It's my great great.... great grandpa's. Twice removed.",
    username = "4N0N"
)

db.session.add_all([post1, post2, post3, post4, post5])
db.session.commit()