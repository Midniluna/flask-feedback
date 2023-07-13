from unittest import TestCase
from flask import session

from app import app
from models import db, User, Feedback

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['WTF_CSRF_ENABLED'] = False

class UserTestCase(TestCase):
    """Tests user creation, login validation, and userpage"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.app_context = app.app_context()
        cls.app_context.push()

        # Create all tables in the database
        db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        db.drop_all()

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        password = "unhashedpass"
        register = User.register(username="belladonna89", pwd=password, email="bella.donna@email.com", first_name="Bella", last_name="Donna")
        # username password email first_name last_name
        db.session.add(register)
        db.session.commit()

        self.unhashedpass = password
        self.user = register

    def tearDown(self):
        """Clean up fouled transactions."""
        
        db.session.rollback()

    def test_homepage(self):
        with app.test_client() as client:

            resp = client.get('/homepage', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Register", html)
            self.assertIn("Login", html)


    def test_register_user(self):
         with app.test_client() as client:
            with client.session_transaction() as sess:
                
                unhashed = "Tacocat"
                resp = client.post('/register', data={'username' : "21Anagram12", 'password' : unhashed, "email" : "iloveanagrams@email.com", "first_name" : "Raven", "last_name" : "Nevar"})
                sess['username'] = "21Anagram12"
                self.assertEqual(resp.status_code, 302)

                user = User.query.filter_by(username="21Anagram12").first()
                self.assertNotEqual(unhashed, user.password)

                new_resp = client.get(f'/users/{user.username}')
                self.assertEqual(new_resp.status_code, 200)

    def test_login_user(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                user = User.query.filter_by(username=self.user.username).first()


                client.post('/login', data={'username' : user.username, 'password' : self.unhashedpass})

                sess['username'] = user.username

                res = client.get(f"/users/{user.username}", follow_redirects = True)
                self.assertEqual(res.status_code, 200)
                html = res.get_data(as_text=True)

                self.assertIn(f"Welcome, {user.username}", html)
                self.assertIn("Logout", html)
                self.assertNotIn("Register", html)
                self.assertNotEqual(user.password, self.unhashedpass)

                sess.pop("username")

    def test_unauthorized(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:

                # No user logged in
                resp1 = client.get(f"/users/{self.user.username}", follow_redirects = True)
                html1 = resp1.get_data(as_text=True)
                self.assertIn("Please Login", html1)

                # Unauthorized user trying to view other user's details page
                resp2 = client.post('/register', data={'username' : "Unauth5", 'password' : "newPassword", "email" : "iaminvalid@email.com", "first_name" : "Yikes", "last_name" : "Whoopsies"})
                sess['username'] = "Unauth5"
                self.assertEqual(resp2.status_code, 302)

                user = User.query.filter_by(username="Unauth5").first()

                sess['username'] = user.username

                resp3 = client.get(f"/users/{self.user.username}", follow_redirects = True)
                html2 = resp3.get_data(as_text=True)

                self.assertIn("You are unauthorized to do that", html2)

# test user registration
# test new 
# test that users other than setup user cannot view setup user's page, delete feedback, edit feedback, etc