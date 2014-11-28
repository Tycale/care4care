# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class CreateBranch(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_create_branch(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Branches")
        sel.click(u"link=Créer une branche")
        sel.wait_for_page_to_load("30000")
        sel.type("id=id_name", "Bruxelles")
        sel.click("css=p")
        sel.type("id=id_location_input", "Bruxelles, Belgique")
        sel.click("//button[@type='submit']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
