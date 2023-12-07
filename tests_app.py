import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test that user list is displayed """
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user_form(self):
        """Test that user form is displayed"""
        with app.test_client() as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!--Testing that add user form appears-->", html)

    def test_process_add_user_form(self):
        """Test that on form submission, page redirects to /users"""
        with app.test_client() as c:
            resp = c.post("/users/new",
                          data = {
                              'first_name': 'test2_first',
                              'last_name': 'test2_last',
                              'image_url': ''
                          })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location,"/users")

    def test_process_add_user_form_followed(self):
        """Tests that new user was added to user list after redirect"""
        with app.test_client() as c:
            resp = c.post("/users/new",
                          data = {
                              'first_name': 'test2_first',
                              'last_name': 'test2_last',
                              'image_url': ''
                          }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test2_first', html)
    # Focus on making more robust tests if on a time constraint

    def test_show_user_info(self):
        """Test that user detail page is displayed"""
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<!-- Testing: User Detail -->", html)

# Additional future tests: test updating user, test the image (what we submit and what ends up in the database and what shows on the page)
# test for invalid inputs, deleting a user, editting a user