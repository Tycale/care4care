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

        print("test offer help")
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("//section[@id='main-content']/section/div[2]/div[2]/button").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Gent')])[3]").click()
        driver.find_element_by_id("id_category_2").click()
        driver.find_element_by_id("id_category_1").click()
        driver.find_element_by_id("id_category_0").click()
        driver.find_element_by_id("id_date").clear()
        driver.find_element_by_id("id_date").send_keys("18/12/2014")
        driver.find_element_by_id("id_time_3").click()
        driver.find_element_by_id("id_time_4").click()
        driver.find_element_by_id("id_time_6").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()


        print("modify profile")
        driver.get(self.base_url + "accounts/profile/")
        driver.find_element_by_link_text("Modifier").click()
        #driver.find_element_by_id("id_photo").clear()
        #driver.find_element_by_id("id_photo").send_keys("/Users/Denis/Downloads/dirk.jpg")
        driver.find_element_by_id("id_facebook").clear()
        driver.find_element_by_id("id_facebook").send_keys("https://www.facebook.com/Guy4Europe")
        driver.find_element_by_id("id_offered_job_0").click()
        driver.find_element_by_id("id_offered_job_2").click()
        driver.find_element_by_id("id_offered_job_3").click()
        driver.find_element_by_id("id_languages_0").click()
        driver.find_element_by_id("id_languages_1").click()
        driver.find_element_by_id("id_languages_2").click()
        driver.find_element_by_id("id_have_car_0").click()
        driver.find_element_by_id("id_drive_license_1").click()
        driver.find_element_by_id("id_drive_license_2").click()
        driver.find_element_by_id("id_drive_license_3").click()
        driver.find_element_by_id("id_can_wheelchair_0").click()
        driver.find_element_by_id("id_hobbies").clear()
        driver.find_element_by_id("id_hobbies").send_keys("La Politique")
        driver.find_element_by_id("id_additional_info").clear()
        driver.find_element_by_id("id_additional_info").send_keys("Votez pour moi!")
        driver.find_element_by_id("id_location_input").clear()
        driver.find_element_by_id("id_location_input").send_keys(u"Chaussée de Gand, Molenbeek-Saint-Jean, Belgique")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        print("test ignore user")
        driver.get(self.base_url + "accounts/profile/")
        driver.find_element_by_link_text(u"Utilisateurs ignorés").click()
        driver.find_element_by_css_selector("#ignored > div.row.mt > div.col-lg-12.col-sm-12 > div.panel.panel-default > div.panel-body > div.row.mt > form > div.col-lg-9 > div.form-group > #id_user").clear()
        driver.find_element_by_css_selector("#ignored > div.row.mt > div.col-lg-12.col-sm-12 > div.panel.panel-default > div.panel-body > div.row.mt > form > div.col-lg-9 > div.form-group > #id_user").send_keys("user1")
        driver.find_element_by_name("ignored").click()
        """
        print("test offer help")
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Planter un arbre dans mon jardin").click()
        driver.find_element_by_css_selector("span.glyphicon.glyphicon-gift").click()
        driver.find_element_by_id("id_time_3").click()
        driver.find_element_by_id("id_comment").clear()
        driver.find_element_by_id("id_comment").send_keys("Je suis partant!")
        driver.find_element_by_xpath("//button[@type='submit']").click()"""

        print("test create emergency contact")
        driver.get(self.base_url + "accounts/profile/")
        driver.find_element_by_link_text("Ajouter").click()
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys("Gui")
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys("Tare")
        driver.find_element_by_id("id_location").clear()
        driver.find_element_by_id("id_location").send_keys("Rue des êtres, Bastogne")
        driver.find_element_by_id("id_phone_number").clear()
        driver.find_element_by_id("id_phone_number").send_keys("061213652")
        driver.find_element_by_id("id_mobile_number").clear()
        driver.find_element_by_id("id_mobile_number").send_keys("0494609971")
        driver.find_element_by_id("id_languages_0").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()

        print("test add favorite")
        driver.get(self.base_url + "")
        driver.find_element_by_xpath("//ul[@id='nav-accordion']/li[3]/a").click()
        driver.find_element_by_css_selector("ul.sub > li > span > a").click()
        driver.find_element_by_link_text("Favoris").click()
        driver.find_element_by_id("id_user").send_keys("user3")
        driver.find_element_by_name("favorite").click()

        print("test rejoign branch")
        driver.get(self.base_url + "")
        driver.find_element_by_css_selector("a.dcjq-parent > span").click()
        driver.find_element_by_link_text("Rejoindre une branche").click()
        Select(driver.find_element_by_id("id_id")).select_by_visible_text("Oostende")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        print("test search")
        driver.get(self.base_url + "search/job/")
        driver.find_element_by_id("id_job_type_1").click()
        driver.find_element_by_id("id_category_6").click()
        driver.find_element_by_id("id_receive_help_from_who_0").click()
        driver.find_element_by_id("id_time_3").click()
        driver.find_element_by_id("id_date1").clear()
        driver.find_element_by_id("id_date1").send_keys("14/12/2014")
        driver.find_element_by_id("id_date2").clear()
        driver.find_element_by_id("id_date2").send_keys("20/12/2014")
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
