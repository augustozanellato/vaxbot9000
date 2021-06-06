# VaxBot9000

## Prerequisites
- Python 3.9
- [Poetry](https://python-poetry.org/)
- [latest version of geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.29.1)
- Firefox

## Setup
1. `poetry install`
1. Copy `config.sample.toml` to `config.toml` and edit the following parameters:
    - `az` your local ULSS (example `ulss6`)
    - `service_id` service code you're interested in (can be found by initiating a reservation and when you're asked to choose a service you inspect the service button and check what's the argument to `scegliserv` called by the button's `onclick` attribute)
    - `cf` your Italian fiscal code
    - `num_team` last six digits of your TEAM card
    - `use_tg` wheter to use Telegram to send notifications
    - `tg_token` your Telegram bot token
    - `tg_chat` your Telegram chat_id or the username of the channel where you wish to send the alerts
    - `spawn_new_browser_on_slot_found` wheter to spawn a new browser window every time a slot is found. **WARNING: this can get pretty chaotic**

## Running
`poetry run python -m vaxbot`