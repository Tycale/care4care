# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class OffrirMonAide(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_offrir_mon_aide(self):
        sel = self.selenium
        sel.open("/")
        sel.click("//section[@id='main-content']/section/div/div[2]/button")
        sel.click("xpath=(//a[contains(text(),'Bruxelles')])[3]")
        sel.wait_for_page_to_load("30000")
        sel.type("id=id_title", "Boire un verre")
        sel.select("id=id_category", "label=Tenir compagnie")
        sel.click("css=span.input-group-addon")
        sel.click("//div[@id='sizcache08657367069560087']/div/div/table/tbody/tr[6]/td[7]")
        sel.click("id=id_time_0")
        sel.click("id=id_time_2")
        sel.click("id=id_time_6")
        sel.type("id=id_estimated_time", "30")
        sel.type("id=id_description", "Juste aller boire un verre")
        sel.click("//section[@id='main-content']/section/div/div/form/div[2]/div/div/div/span/span/div/span/div[2]/p")
        sel.type("id=id_location_input", "Bruxelles Midi, Saint-Gilles, Belgique")
        sel.click("//button[@type='submit']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
