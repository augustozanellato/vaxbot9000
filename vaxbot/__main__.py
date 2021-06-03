from splinter import Browser
from telegram import Bot
from time import sleep
import logging
import toml
import os.path

config = toml.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'config.toml'))
bot = None
if config['use_tg']:
    bot = Bot(config["tg_token"])
browser = Browser('firefox', headless=not config['spawn_new_browser_on_slot_found'])
newline = '\n'


def fill_browser(browser):
    global config
    browser.visit(f'https://vaccinicovid.regione.veneto.it/{config["az"]}')
    browser.fill('cod_fiscale', config["cf"])
    browser.fill('num_tessera', config["num_team"])
    browser.find_by_css('div.form-group:nth-child(4) > div:nth-child(2) > input:nth-child(1)').first.check()
    browser.evaluate_script('inviacf();')
    sleep(0.1)
    if "servizio" in browser.find_by_css('#corpo2 > h2').text:
        browser.evaluate_script('scegliserv(641)')

def send_message(text):
    if config['use_tg']:
        bot.send_message(config['tg_chat'], text)

old_slots = []
while True:
    fill_browser(browser)
    available_slots = [button.html.split('<br>')[0].strip() for button in browser.find_by_css('#corpo2 button.btn-primary:not(.btn-back') if 'onclick' in button.outer_html]
    if available_slots != old_slots:
        print(f'slot change: {available_slots}')
        if len(available_slots) == 0:
            send_message(f'Slot terminati!')
        else:
            if config["spawn_new_browser_on_slot_found"]:
                browser = Browser('firefox')
            send_message(f'Slot disponibili:{newline}{newline.join(available_slots)}')
    old_slots = available_slots
    sleep(0.1)