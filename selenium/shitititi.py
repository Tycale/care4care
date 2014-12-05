# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Shitititi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_shitititi(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//ul[@id='nav-accordion']/li[3]/a").click()
        driver.find_element_by_css_selector("ul.sub > li > span > a").click()
        driver.find_element_by_link_text("Favoris").click()
        driver.find_element_by_id("ui-id-11").click()
        driver.find_element_by_id("id_user").clear()
        driver.find_element_by_id("id_user").send_keys("user3")
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("18/12/2014")
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("18/12/2014")
        driver.find_element_by_link_text("Branches").click()
        driver.find_element_by_link_text("Gent").click()
        driver.find_element_by_link_text("J'ai besoin d'aide").click()
        driver.find_element_by_link_text("Offrir mon aide").click()
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("18/12/2014")
        driver.find_element_by_id("id_time_0").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_name("favorite").click()
        driver.find_element_by_id("id_time_1").click()
        driver.find_element_by_id("id_time_3").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
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
