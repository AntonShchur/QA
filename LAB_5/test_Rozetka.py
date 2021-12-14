from page_objects import *
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


class Test_rozetka(TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://rozetka.com.ua/ua/")
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def test_search_button(self):
        text_to_search = "rtx 3080"
        main_page = SearchHelper(self.driver)
        main_page.enter_text(text_to_search)
        main_page.click_on_the_search_button()
        assert text_to_search.lower() in main_page.find_text().lower()

    def test_search_field(self):
        text_to_search = "rtx 3070"
        main_page = SearchHelper(self.driver)
        main_page.enter_text(text_to_search)
        main_page.enter_text(Keys.ENTER)
        assert text_to_search.lower() in main_page.find_text().lower()

    def test_goods_filter(self):
        filter_name = "Комп'ютери та ноутбуки"
        filter_menu = CategoryFilter(self.driver)
        filter_menu.click_on_filter_menu()
        filter_menu.click_on_pc_category()
        response_category_name = filter_menu.find_text()
        assert response_category_name.lower() == filter_name.lower()

    def tearDown(self) -> None:
        self.driver.close()
