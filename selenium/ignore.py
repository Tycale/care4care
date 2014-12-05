# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Ignore(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ignore(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_link_text("Mon Profil").click()
        driver.find_element_by_link_text(u"Utilisateurs ignorés").click()
        driver.find_element_by_id("ui-id-9").click()
        driver.find_element_by_css_selector("#ignored > div.row.mt > div.col-lg-12.col-sm-12 > div.panel.panel-default > div.panel-body > div.row.mt > form > div.col-lg-9 > div.form-group > #id_user").clear()
        driver.find_element_by_css_selector("#ignored > div.row.mt > div.col-lg-12.col-sm-12 > div.panel.panel-default > div.panel-body > div.row.mt > form > div.col-lg-9 > div.form-group > #id_user").send_keys("user4")
        driver.find_element_by_name("ignored").click()
    
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