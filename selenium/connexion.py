# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class Connexion(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_connexion(self):
        sel = self.selenium
        sel.open("/accounts/register/complete/")
        sel.click("xpath=(//button[@type='button'])[2]")
        sel.type("id=username", "Denis")
        sel.type("id=password", "denis")
        sel.click("//button[@type='submit']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
