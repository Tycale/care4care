# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class AjouterUnContactDUrgence(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_ajouter_un_contact_d_urgence(self):
        sel = self.selenium
        sel.open("/accounts/profile/1/")
        sel.click("link=Ajouter")
        sel.wait_for_page_to_load("30000")
        sel.type("id=id_first_name", "Victor")
        sel.type("id=id_last_name", "Velghe")
        sel.type("id=id_location", "Charleroi")
        sel.type("id=id_phone_number", "0494602972")
        sel.type("id=id_mobile_number", "0494602341")
        sel.click("id=id_languages_0")
        sel.select("id=id_order", "label=A contacter en dernier")
        sel.click("//button[@type='submit']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
