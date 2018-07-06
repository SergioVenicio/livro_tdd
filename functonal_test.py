import unittest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self._path = FirefoxBinary('/opt/firefox/firefox')
        self.browser = webdriver.Firefox(firefox_binary=self._path)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_letter(self):
        # Edith ouviu falar de uma nova aplicação online interessante para
        # lista de tarefas. Ela decide verificar sua homepage
        self.browser.get('http://localhost:8000/')

        # Ela percebe que o titulo da página e o cabeçalho mencionam listas de
        # taferefas (to-do)
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main()
