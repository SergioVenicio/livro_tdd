from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

browser_path = FirefoxBinary('/opt/firefox/firefox')
browser = webdriver.Firefox(firefox_binary=browser_path)
browser.get('http://localhost:8000')

assert 'Django' in browser.title
