import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
import db_manager
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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("THIS IS TEST BOT. MOST OF FUNCTIONAL NOT AVAILABLE. WE FIXED IT SOON")
    with open('media/uk-postcode-components.gif', 'rb') as photo:
        await message.answer_photo(photo, caption="Hi, I know about power cuts in London. Just send me your postcode "
                                                  "and "
                                                  "I'm checking power incidents in your borough.")


@dp.message_handler()
async def get_incidents(message: types.Message):
    response = session.get('https://www.ukpowernetworks.co.uk/api/power-cut/all-incidents')
    # result = session.get('https://swapi.dev/api/')
    print("Time: {0} / Used Cache: {1}".format(response.headers["Date"], response.from_cache))
    incidents = powercuts.search_by_postcode(message.text, response.json())
    if incidents:
        textForUser = ''
        for incident in incidents:
            textForUser += f"Incident Reference: {incident['incidentReference']}\nPower Cut Type: {incident['powerCutType']}\nDescription: {incident['incidentCategoryCustomerFriendlyDescription']}\n\n{incident['ukpnIncident']['mainMessage']}\n\n\n\n"
            textForUser2 = f"По вашему запросу найдено {len(incidents)} проишествий\n\n\n\n{textForUser}"
            print("ДЛИНА СООБЩЕНИЯ ", len(textForUser2))
        if len(textForUser2) < 4000:
            await message.answer(f"По вашему запросу найдено {len(incidents)} проишествий\n\n\n\n{textForUser}")
        else:
            limit = 4000
            chunks = [str[i:i + limit] for i in range(0, len(str), limit)]
            for part in chunks:
                await message.answer(part)

    else:
        await message.answer("По вашему запросу ничего не найдено")


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

from api_manager import ApiPowerCuts
import db_manager
# result = ApiPowerCuts.get_incidents_list()
# print(result.json())
# import powercuts

# db_manager.insert_user(99585850989)
#
# l = powercuts.search_by_postcode('')
# print(len(l))
# print(list(l.keys()))
