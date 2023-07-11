from unittest import TestCase

from app import app
from models import db, User



# class UserCreationTestCase(TestCase):
#     """Tests for User creation."""

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()

#         cls.app_context = app.app_context()
#         cls.app_context.push()

#         # Create all tables in the database
#         db.create_all()

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()

#     def setUp(self):
#         """Make demo data."""

#         User.query.delete()

#         user = User(username="belladonna", password="hashedpass", email="bella.donna@email.com", first_name="Bella", last_name="Donna")
#         # username password email first_name last_name
#         db.session.add(user)
#         db.session.commit()

#         self.user = user

#     def tearDown(self):
#         """Clean up fouled transactions."""

#         db.session.rollback()

#     def test_user(self):
#         with app.test_client() as client:
#             resp = client.get("")