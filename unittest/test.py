import unittest, sys
import os

sys.path.append('../QuizMeFinal') # imports python file from parent directory

from run import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    # def test_main_page(self):
    #     response = self.app.get('/', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    
    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_signup(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_started(self):
        response = self.app.get('/getstarted', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_flashcards(self):
        response = self.app.get('/createflashcards', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    
    def test_your_flashcards(self):
        response = self.app.get('/your-flashcards', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_success(self):
        response = self.app.get('/success', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # def test_single_flashcard(self):
    #     response = self.app.get('/single-flashcard', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    
    def test_single_about_us(self):
        response = self.app.get('/aboutus', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
if __name__ == "__main__":
    unittest.main()