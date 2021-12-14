from selenium.webdriver.common.by import By


class MainPageLocators:
    SEARCH_BUTTON = (By.CLASS_NAME, "button")
    SEARCH_FORM = (By.CLASS_NAME, "search-form")
    SEARCH_FIELD = (By.CLASS_NAME, "search-form__input")


class SearchResultPageLocators:
    GOOD_NAME = (By.CLASS_NAME, "goods-tile__title")
    PORTAL_HEADING = (By.CLASS_NAME, "portal__heading")


class FilterLocators:
    FAT_MENU = (By.ID, "fat-menu")

    NOTEBOOKS_PC = (By.LINK_TEXT, 'Ноутбуки та комп’ютери')
