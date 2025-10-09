import unittest
from lib.router import Router
from main import DevPortfolio

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.app = DevPortfolio().app
        Router(self.app)
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    def test_projects_GET(self):
        response = self.client.get("/api/projects")
        self.assertEqual(response.status_code, 200)
    
    def test_about_GET(self):
        response = self.client.get("/api/about")
        self.assertEqual(response.status_code, 200)
    
    def test_feedback_GET(self):
        response = self.client.get("/api/feedback")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()