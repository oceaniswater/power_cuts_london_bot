import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
import api_manager
import powercuts
from requests_cache import CachedSession

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(disdpatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

@dp.message_handler(commands=['test'])
async def send_incident(message: types.Message):
    incident = api_manager.ApiPowerCuts.get_incident_by_id('INCD-320571-Z')
    incident = incident.json()
    print(incident)
    textForUser2 = f"Incident Reference: {incident['result']['incidentReference']}\n\n" \
                   f"Power Cut Type: {incident['result']['powerCutType']}\n" \
                   f"Detected time: {incident['result']['ukpnIncident']['receivedDate']}\n" \
                   f"Estimated Restoration Date: {incident['result']['ukpnIncident']['estimatedRestorationDate'] if incident['result']['ukpnIncident']['estimatedRestorationDate'] is not None else 'Date unknown'}\n" \
                   f"Description: {incident['result']['ukpnIncident']['incidentCategoryCustomerFriendlyDescription']}\n" \
                   f"Actual status: {[step['message'] for step in incident['result']['steps'] if incident['result']['steps']['active'] == True]}\n"
    if len(textForUser2) < 4000:
        await message.answer(textForUser2)
    else:
        limit = 4000
        chunks = [textForUser2[i:i + limit] for i in range(0, len(textForUser2), limit)]
        for part in chunks:
            await message.answer(part)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    with open('media/uk-postcode-components.gif', 'rb') as photo:
        await message.answer_photo(photo, caption="Hi, I am Powerbot and I know about power cuts in London. Just send "
                                                  "me your postcode or a part of it and "
                                                  "I will check power incidents in your borough.\n\nThis is an "
                                                  "unofficial bot which takes open data from Distribution Network "
                                                  "Operator | UK Power Networks")


@dp.message_handler()
async def get_incidents(message: types.Message):
    response = session.get('https://www.ukpowernetworks.co.uk/api/power-cut/all-incidents')
    print("Time: {0} / Used Cache: {1}".format(response.headers["Date"], response.from_cache))
    incidents = powercuts.search_by_postcode(message.text, response.json())
    if incidents:
        textForUser = ''
        for incident in incidents:
            textForUser += f"Incident Reference: {incident['incidentReference']}\n\nPower Cut Type: {incident['powerCutType']}\nDescription: {incident['incidentCategoryCustomerFriendlyDescription']}\nPost codes affected: {incident['ukpnIncident']['postCodesAffected']}\n\n"
        textForUser2 = f"Detected {len(incidents)} incidents:\n{textForUser}"
        if len(textForUser2) < 4000:
            await message.answer(textForUser2)
        else:
            limit = 4000
            chunks = [textForUser2[i:i + limit] for i in range(0, len(textForUser2), limit)]
            for part in chunks:
                await message.answer(part)
    else:
        await message.answer("There are no incidents. But if you are without power now. Contact UK Power "
                             "Networks.\n\n08003163105 or 105\n\nFree to call from a mobile or a landline phone\n\n")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    session = CachedSession('test_cache', backend='sqlite', expire_after=600)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
