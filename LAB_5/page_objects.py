from base_page import BasePage
from locators import *


class SearchHelper(BasePage):

    def enter_search_term(self, text):
        search_field = self.find_element(MainPageLocators.SEARCH_FIELD)
        search_field.send_keys(text)
        return search_field

    def click_on_the_search_button(self):
        self.driver.find_element(*MainPageLocators.SEARCH_FORM).find_element(*MainPageLocators.SEARCH_BUTTON)\
            .click()

    def find_text(self):
        return self.find_element(SearchResultPageLocators.GOOD_NAME).text


class CategoryFilter(BasePage):

    def click_on_filter_menu(self):
        self.find_element(FilterLocators.FAT_MENU).click()

    def click_on_pc_category(self):
        self.find_element(FilterLocators.NOTEBOOKS_PC).click()

    def find_text(self):
        return self.find_element(SearchResultPageLocators.PORTAL_HEADING).text
