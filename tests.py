import unittest
from lib.router import Router
from main import DevPortfolio

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.app = DevPortfolio().app
        Router(self.app)
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    def test_projects_endpoint(self):
        response = self.client.get("/projects/raw")
        self.assertEqual(response.status_code, 200)
    
    def test_about_endpoint(self):
        response = self.client.get("/about/raw")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()