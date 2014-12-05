# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class User(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_user(self):
        print("test connexion")
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("user2")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("user2")
        driver.find_element_by_xpath("//button[@type='submit']").click()


        print("test search")
        driver.get(self.base_url + "search/job/")
        driver.find_element_by_id("id_job_type_1").click()
        driver.find_element_by_id("id_category_6").click()
        driver.find_element_by_id("id_receive_help_from_who_0").click()
        driver.find_element_by_id("id_time_3").click()
        driver.find_element_by_id("id_date1").clear()
        driver.find_element_by_id("id_date1").send_keys("21/12/2014")
        driver.find_element_by_id("id_date2").clear()
        driver.find_element_by_id("id_date2").send_keys("20/12/2014")
        driver.set_page_load_timeout(10)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        print("test user search")
        driver.get(self.base_url + "")
        driver.find_element_by_name("q").clear()
        driver.set_page_load_timeout(10)
        driver.find_element_by_name("q").send_keys("user")


    
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
