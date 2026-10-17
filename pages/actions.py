
import allure
from playwright.sync_api import Page, expect

class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста в поле: {locator}")
    def enter_text(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator: str):
        self.page.click(locator)

    @allure.step("Проверка текста элемента {locator}: {text}")
    def assert_text(self, locator: str, text: str):
        expect(self.page.locator(locator)).to_have_text(text)

    @allure.step("Проверка, что виден текст: {text}")
    def assert_text_visible(self, text: str, exact: bool = False):
        expect(self.page.get_by_text(text, exact=exact)).to_be_visible()

    @allure.step("Выбор пункта списка: {name}")
    def select_list_option(self, name: str):
        self.page.get_by_role("listbox").get_by_role("option", name=name, exact=True).click()


    @allure.step("Обновление страницы")
    def reload(self):
        self.page.reload()

    @allure.step("Ожидание появления элемента: {locator}")
    def wait_for_visible(self, locator: str):
        self.page.locator(locator).wait_for(state="visible")

    @allure.step("Проверка, что виден текст: {text}")
    def assert_text_visible(self, text: str, exact: bool = False):
        expect(self.page.get_by_text(text, exact=exact)).to_be_visible()