# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ModifyProfile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_modify_profile(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_link_text("Mon Profil").click()
        driver.find_element_by_link_text("Modifier").click()
        driver.find_element_by_id("id_photo").clear()
        driver.find_element_by_id("id_photo").send_keys("/Users/Denis/Downloads/dirk.jpg")
        driver.find_element_by_id("id_facebook").clear()
        driver.find_element_by_id("id_facebook").send_keys("https://www.facebook.com/dirk.frimout.568?fref=ts")
        driver.find_element_by_id("id_offered_job_0").click()
        driver.find_element_by_id("id_offered_job_4").click()
        driver.find_element_by_id("id_offered_job_6").click()
        driver.find_element_by_id("id_languages_0").click()
        driver.find_element_by_id("id_languages_1").click()
        driver.find_element_by_id("id_languages_2").click()
        driver.find_element_by_id("id_have_car_0").click()
        driver.find_element_by_id("id_drive_license_1").click()
        driver.find_element_by_id("id_drive_license_2").click()
        driver.find_element_by_id("id_drive_license_3").click()
        driver.find_element_by_id("id_can_wheelchair_0").click()
        driver.find_element_by_id("id_hobbies").clear()
        driver.find_element_by_id("id_hobbies").send_keys("Aller dans l'espace")
        driver.find_element_by_id("id_additional_info").clear()
        driver.find_element_by_id("id_additional_info").send_keys("Je suis astronaute")
        driver.find_element_by_id("id_location_input").clear()
        driver.find_element_by_id("id_location_input").send_keys(u"Chaussée de Gand, Molenbeek-Saint-Jean, Belgique")
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
