from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(1, 50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(1, 30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(1, 30)])
    # username password email first_name last_name

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Title", validators=[InputRequired()])