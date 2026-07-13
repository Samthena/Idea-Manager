import os
import unittest

from Omnilinx import app, db


class IdeaListingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_new_idea_is_rendered_after_post(self):
        response = self.client.post('/', data={
            'title': 'New Idea',
            'description': 'A test idea',
            'client': 'Client A',
            'meeting_date': '2026-07-13T10:00',
            'owner': 'Owner A'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Idea', response.data)
        self.assertIn(b'Client A', response.data)


if __name__ == '__main__':
    unittest.main()
