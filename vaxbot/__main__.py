import os.path
import sys
import typing
from time import sleep

import toml
from bs4 import BeautifulSoup
from requests import Session

config_filename = "config.toml"
if len(sys.argv) > 1:
    config_filename = sys.argv[1]
config = toml.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.toml"))
base_url = f'https://vaccinicovid.regione.veneto.it/{config["az"]}'
bot = None
if config["use_tg"]:
    from telegram import Bot

    bot = Bot(config["tg_token"])

if config["spawn_new_browser_on_slot_found"]:
    from splinter import Browser


def fill_browser(browser):
    global config
    browser.visit(base_url)
    browser.fill("cod_fiscale", config["cf"])
    browser.fill("num_tessera", config["num_team"])
    browser.find_by_css("div.form-group:nth-child(5) > div:nth-child(2) > input:nth-child(1)").first.check()
    browser.evaluate_script("inviacf();")
    sleep(0.3)
    browser.evaluate_script(f'scegliserv({config["service_id"]})')


def send_message(text):
    if config["use_tg"]:
        bot.send_message(config["tg_chat"], text)


old_slots = []
while True:
    try:
        session = Session()
        session.post(
            f"{base_url}/azione/controllocf",
            data={
                "cod_fiscale": config["cf"],
                "num_tessera": config["num_team"],
            },
        )
        slots_soup = BeautifulSoup(
            session.post(f'{base_url}/azione/sceglisede/servizio/{config["service_id"]}').content, "lxml"
        )
        available_slots = [
            button.contents[0].strip()
            for button in slots_soup.select("button.btn-primary:not(.btn-back)")
            if button.has_attr("onclick")
        ]
        if available_slots != old_slots:
            print(f"slot change: {available_slots}")
            if len(available_slots) == 0:
                send_message(f"Slot terminati!")
            else:
                if config["spawn_new_browser_on_slot_found"]:
                    fill_browser(Browser("firefox"))
                send_message(f"Slot disponibili:\n{chr(10).join(available_slots)}")
        old_slots = available_slots
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    finally:
        sleep(1)
