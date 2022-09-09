import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
import api_manager
import powercuts
from requests_cache import CachedSession
import keyboards

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

async def get_incident(message: types.Message, id):
    incident = api_manager.ApiPowerCuts.get_incident_by_id(id)
    incident = incident.json()
    textForUser2 = f"Incident Reference: {incident['result']['incidentReference']}\n\n" \
                   f"Power Cut Type: {incident['result']['powerCutType']}\n" \
                   f"Detected time: {incident['result']['ukpnIncident']['receivedDate']}\n\n" \
                   f"Estimated Restoration Date: {incident['result']['ukpnIncident']['estimatedRestorationDate'] if incident['result']['ukpnIncident']['estimatedRestorationDate'] is not None else 'Date unknown'}\n\n" \
                   f"Description: {incident['result']['incidentCategoryCustomerFriendlyDescription']}\n" \
                   f"Actual status: {[step['message'] for step in incident['result']['steps'] if step['active'] == True]}\n"
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

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('INCD'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

@dp.message_handler()
async def get_incidents(message: types.Message):
    response = session.get('https://www.ukpowernetworks.co.uk/api/power-cut/all-incidents')
    print("Time: {0} / Used Cache: {1}".format(response.headers["Date"], response.from_cache))
    incidents, incidentsIds = powercuts.search_by_postcode(message.text, response.json())
    if incidents:
        textForUser = ''
        for incident in incidents:
            textForUser += f"Incident Reference: {incident['incidentReference']}\n\nPower Cut Type: {incident['powerCutType']}\nDescription: {incident['incidentCategoryCustomerFriendlyDescription']}\nPost codes affected: {incident['ukpnIncident']['postCodesAffected']}\n\n"
        textForUser2 = f"Detected {len(incidents)} incidents:\n{textForUser}"
        if len(textForUser2) < 4000:
            await message.answer(textForUser2, reply_markup=keyboards.make_inline_keybord(incidentsIds))
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
