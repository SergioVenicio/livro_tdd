import os
import re
import time
import poplib
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

        # Agora ela faz o logout
        self.browser.find_element_by_link_text('Logout').click()


        # Ela não está mais logada!
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')

        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                # Obtem as 10 menssagens mais recentes
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('Getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf-8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)

            inbox.quit()
