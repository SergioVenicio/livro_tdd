from datetime import time
from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith acessa a página inicial e acideltalmente tenta submeter
        # um item vazio na lista. Ela tecla Enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # O carregador intercepta a requisição e não carrega a página da lista
        # que itens da lista não podem está em branco.
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # Ela começa a digitar um texto para o novo item e o erro desaparece
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # Ela pode submeter o item com sucesso
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # De forma peversa, ela agora decide submeter um segundo item
        # em branco na lista
        self.get_item_input_box().send_keys(Keys.ENTER)

        # E ela pode corrigir isso preenchendo o item com um texto
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith acessa a página inicial e começa uma nova lista
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')


        # Ela tenta acidentalmente inserir um item duplicado
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela vê uma mensagem de erro prevista
        self.wait_for(lambda : self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith inicia uma lista e provoda um erro de validação:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Ela começa a digitar na caixa de entrada para limpar o erro
        self.get_item_input_box().send_keys('a')

        # Ela fica satisfeita ao ver que a menssagem de erro desaparece
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))