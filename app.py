from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from IPython import embed

from models import db, connect_db, get_database_uri, get_echo_TorF, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = get_echo_TorF()
app.config["SECRET_KEY"] = "thisIsASecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)



@app.route('/')
def direct_home():
    return redirect('/register')

@app.route('/homepage')
def home_page():
    if 'username' not in session:
        flash("Please register or login", "danger")
        return redirect('/register')
    return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Create a new user"""

    if "username" in session:
        
        return redirect(f"/users/{session['username']}")
    
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username or email taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash("Welcome! Successfully Created Your Account!", "success")
        return redirect(f"/users/{session['username']}")

    return render_template('register.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Validate credentials, log in user"""
    
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginUserForm()
    
    if form.validate_on_submit():
        username= form.username.data
        password= form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/users/{session['username']}")
        else:
            form.username.errors = ["Invalid username or password."]

    return render_template('login.html', form = form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')

@app.route('/users/<username>')
def view_userpage(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.all()
    return render_template('secret.html', user=user, feedback=feedback)

@app.route('/users/<username>/delete')
def delete_user(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')
    
    User.query.filter_by(username=username).first().delete()
    session.pop('username')
    return redirect('/login')


# ------- FEEDBACK ROUTES ---------


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    
    post = Feedback.query.get(feedback_id)
    username = post.user.username

    if "username" not in session:
        return redirect('/login')
    elif username != session['username']:
        return redirect(f'/users/{username}')
    
    form = FeedbackForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('edit-post.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    post = Feedback.query.get(feedback_id)
    db.session.delete(post)
    db.session.commit()
    return "Deleted!"

# Barksley123 woofwoof
