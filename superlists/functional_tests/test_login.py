import re
from django.core import mail
from .base import FunctionalTest
from django.utils.html import escape
from selenium.webdriver.common.keys import Keys


TEST_EMAIL = 'sergioandradeteste@gmail.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Edith acessa o incrível site de superlistas
        # e, pela primeira vez, percebe que há uma seção de "Log in" na barra
        # de navegação. Essa seção está lhe dizendo para inserir o endereço
        # de email, portanto ela faz isso
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Uma menssagem aparece informando-lhe que um email foi enviado
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            escape(self.browser.find_element_by_tag_name('body').text)
        ))

        # Ela verifica seu email e encontra uma menssagem
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # A menssagem contém um link com um url
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Ela clica no url
        self.browser.get(url)

        # Ela está logada!
        self.wait_for(
            lambda : self.browser.find_element_by_link_text('Logout')

        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, escape(navbar.text))