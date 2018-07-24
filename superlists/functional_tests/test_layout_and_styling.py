from .base import FunctionalTest, webdriver
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith acessa a página inicial
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ela percebe que a caixa de entrada está elegantemente centralizada
        input_box = self.browser.find_element_by_id('id_new_item')

        # Ela inicia uma nova lista e vê que a entrada está elegantemente
        # centralizada aí também
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: testing')

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512, delta=100
        )
