import unittest
import chromedriver_binary
from selenium import webdriver

class NewVisitorTests(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        
    def tearDown(self):
        self.browser.quit()
        
    def test_user_visited(self):
        '''
        ・ユーザはサイトにアクセスする
        ・ページタイトルがDjangoであることを確認する。
        '''
        
        self.browser.get('http:127.0.0.1:8000')
        self.assertIn('Blog', self.browser.title)
        
        
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')