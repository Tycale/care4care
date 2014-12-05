# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class CreateEmergency(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_emergency(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_link_text("Mon Profil").click()
        driver.find_element_by_link_text("Ajouter").click()
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys("Denis")
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys("Genon")
        driver.find_element_by_id("id_location").clear()
        driver.find_element_by_id("id_location").send_keys("Savy, Bastogne")
        driver.find_element_by_id("id_phone_number").clear()
        driver.find_element_by_id("id_phone_number").send_keys("061213632")
        driver.find_element_by_id("id_mobile_number").clear()
        driver.find_element_by_id("id_mobile_number").send_keys("0494602971")
        driver.find_element_by_id("id_languages_0").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
