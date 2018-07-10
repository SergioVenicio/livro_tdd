import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self._path = FirefoxBinary('/opt/firefox/firefox')
        self.browser = webdriver.Firefox(firefox_binary=self._path)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_letter(self):
        # Edith ouviu falar de uma nova aplicação online interessante para
        # lista de tarefas. Ela decide verificar sua homepage
        self.browser.get('http://localhost:8000/')

        # Ela percebe que o titulo da página e o cabeçalho mencionam listas de
        # taferefas (to-do)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'), 'Enter a to-do item'
        )

        # Ela digita "Buy peacock feathers" em uma caixa de texto
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        input_box.send_keys('Use peacock to make a fly')
        input_box.send_keys(Keys.ENTER)

        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy peacock feathers'),
        self.check_for_row_in_list_table('2: Use peacock to make a fly'),

        # Edith se pergunta se o site lembrará de sua lista. Então ela nota
        # que o site gerou um url único para ela
        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main()
