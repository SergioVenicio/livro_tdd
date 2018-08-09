import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise(e)
                else:
                    time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self._path = FirefoxBinary('/opt/firefox/firefox')
        self.browser = webdriver.Firefox(firefox_binary=self._path)
        staging_server = os.environ.get('STAGING_SERVER')

        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Logout')
        )

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)