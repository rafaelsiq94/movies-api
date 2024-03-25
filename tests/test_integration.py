import unittest
from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_movies(self):
        response = self.app.get('/movies')
        data = response.json
        expected_length = 206
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), expected_length)

    def test_get_movies_max_min_win_interval_for_producers(self):
        response = self.app.get('/movies?projection=max-min-win-interval-for-producers')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['min'][0]['interval'], 1)
        self.assertEqual(data['max'][0]['interval'], 13)


if __name__ == '__main__':
    unittest.main()
