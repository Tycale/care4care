# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class Modifier le profil(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_modifier le profil(self):
        sel = self.selenium
        sel.open("/")
        sel.click("//button[@type='button']")
        sel.click("link=Mon Profil")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Modifier")
        sel.wait_for_page_to_load("30000")
        sel.click("id=id_email")
        sel.type("id=id_email", "denis@gmail.com")
        sel.select("id=id_status", "label=Actif")
        sel.select("id=id_status", "label=En vacance")
        sel.click("id=id_offered_job_3")
        sel.click("id=id_offered_job_4")
        sel.click("id=id_offered_job_1")
        sel.type("id=id_additional_info", u"Je préfère etre contacté par e-mail")
        sel.type("id=id_hobbies", "Le Basketball")
        sel.click("id=id_have_car_0")
        sel.click("id=id_drive_license_2")
        sel.click("id=id_drive_license_2")
        sel.click("id=id_drive_license_5")
        sel.click("id=id_drive_license_5")
        sel.click("id=id_can_wheelchair_0")
        sel.click("//button[@type='submit']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
