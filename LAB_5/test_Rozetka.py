from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure

class Test_Rozetka(TestCase):
    def test_rozetka(self):
        search_text = 'rtx 3080'
        url = "https://rozetka.com.ua/ua/"
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.implicitly_wait(10)

        browser.get(url)
        browser.find_element(by=By.CLASS_NAME, value='search-form__input').send_keys(search_text)
        browser.find_element(by=By.CLASS_NAME, value='search-form__input').send_keys(Keys.ENTER)
        response = browser.find_element(by=By.CLASS_NAME, value='goods-tile__title').text

        assert search_text in response.lower()
        browser.close()


    def test_filter_rozetka(self):
        filter_name = "Комп'ютери та ноутбуки"
        url = "https://rozetka.com.ua/ua/"
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.implicitly_wait(10)
        browser.maximize_window()

        browser.get(url)
        browser.find_element(by=By.ID, value="fat-menu").click()
        browser.implicitly_wait(10)
        browser.find_element(by=By.LINK_TEXT, value="Ноутбуки та комп’ютери").click()
        browser.implicitly_wait(10)
        response = browser.find_element(by=By.CLASS_NAME, value="portal__heading").text
        assert response == filter_name

        browser.close()


    def test_search_button(self):
        search_text = 'rtx 3080'
        url = "https://rozetka.com.ua/ua/"
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.maximize_window()

        browser.implicitly_wait(10)
        browser.get(url)
        browser.find_element(by=By.CLASS_NAME, value='search-form__input').send_keys(search_text)
        browser.find_element(by=By.CLASS_NAME, value="search-form").find_element(by=By.CLASS_NAME, value="button").click()
        response = browser.find_element(by=By.CLASS_NAME, value='goods-tile__title').text
        assert search_text in response.lower()

        browser.close()
