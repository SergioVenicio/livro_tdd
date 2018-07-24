from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith acessa a página inicial e acideltalmente tenta submeter
        # um item vazio na lista. Ela tecla Enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.Enter)

        # A página é atualizada e há uma menssagem de erro informando
        # que itens da lista não podem está em branco.
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has_error').text,
                "You can't have a empty list item"
            )
        )

        # Ela tenta novamente com um texto para o item, e agora funciona
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # De forma peversa, ela agora decide submeter um segundo item
        # em branco na lista
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Ela recebe um aviso semelhante na página da lista
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has_error').text,
                "You can't have a empty list item"
            )
        )

        # E ela pode corrigir isso preenchendo o item com um texto
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')