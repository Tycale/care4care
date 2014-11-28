# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class Inscription(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_inscription(self):
        sel = self.selenium
        sel.open("/")
        sel.click("//button[@type='button']")
        sel.wait_for_page_to_load("30000")
        sel.type("id=id_username", "DenisGenon")
        sel.type("id=id_password1", "denis")
        sel.type("id=id_password2", "denis")
        sel.type("id=id_first_name", "Denis")
        sel.type("id=id_last_name", "Genon")
        sel.select("id=id_birth_date_day", "label=15")
        sel.select("id=id_birth_date_month", u"label=décembre")
        sel.select("id=id_birth_date_year", "label=1991")
        sel.type("id=id_email", "denisgenon@gmail.com")
        sel.type("id=id_phone_number", "061213632")
        sel.type("id=id_mobile_number", "0494602971")
        sel.click("id=id_how_found_0")
        sel.click("id=id_how_found_2")
        sel.select("id=id_id", "label=Louvain-la-Neuve")
        sel.click("xpath=(//button[@type='submit'])[2]")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
