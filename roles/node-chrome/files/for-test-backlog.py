#! /usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import timeout_decorator
import json


def register_whitelist(browser):
    # Access to siteblock setting page
    browser.get('chrome-extension://pfglnpdpgmecffbejlfgpnebopinlclj/html/options.html')

    # Find the siteblock elements
    siteblockRulesXpath='//textarea[@id="rules"]'
    siteblockSubmitXpath='//input[@id="submit"]'
    siteblockRules = browser.find_element(by=By.XPATH, value=siteblockRulesXpath)
    siteblockSubmit = browser.find_element(by=By.XPATH, value=siteblockSubmitXpath)

    siteblockRules.clear()

    rulesStr = os.environ.get('RULES')
    rules = json.loads(rulesStr)
    sendRulesStr = '*'
    for rule in rules:
        sendRulesStr = sendRulesStr + '\n+' + rule

    siteblockRules.send_keys(sendRulesStr)
    siteblockSubmit.click()


def access_backlog(browser):
    # Access to Backlog
    browser.get('https://procube.backlog.jp/')
    
    # Find the elements
    userIdXpath='//input[@id="userId"]'
    passwordXpath='//input[@id="password"]'
    submitXpath='//input[@id="submit"]'

    userId = browser.find_element(by=By.XPATH, value=userIdXpath)
    password = browser.find_element(by=By.XPATH, value=passwordXpath)
    submit = browser.find_element(by=By.XPATH, value=submitXpath)

    # Clear the text box
    userId.clear()
    password.clear()

    # Input the text box
    userId.send_keys(os.environ.get('USERNAME'))
    password.send_keys(os.environ.get('PASSWORD'))

    # Click the submit button
    time.sleep(2)
    submit.click()


@timeout_decorator.timeout(1)
def isChromeExist():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:33871")
    browser = webdriver.Chrome(options=options)


def loginToBacklog():
    #Constract driver
    options = Options()
    options.add_argument('--remote-debugging-port=33871')
    #options.add_argument('--app=https://www.google.com/')
    options.add_extension('/var/lib/crx/0.2.4_0.crx')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja'})
    options.add_experimental_option('detach', True)
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)

    # register_whitelist(browser)
    # access_backlog(browser)

    # while True:
    #     time.sleep(5)
    #     browser.get('https://procube.info/')
    #     time.sleep(5)
    #     access_backlog(browser)

    while True:
        browser.get('http://nginx/')
        time.sleep(5)
        browser.get('http://apache/')
        time.sleep(5)


try:
    isChromeExist()
except timeout_decorator.timeout_decorator.TimeoutError:
    loginToBacklog()