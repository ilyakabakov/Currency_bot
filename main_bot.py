import asyncio
import logging
import os

from handlers import client
from initialize import dp, bot

cwd = os.getcwd()

logging.basicConfig(filename=os.path.join(cwd, 'logs/main.log'))

ALLOWED_UPDATES = [
    'message',
    'edited_message',
    'callback_query'
]
async def if_started():
    try:
        print('Bot is ONLINE')
        dp.include_router(
            client.router
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               allowed_updates=ALLOWED_UPDATES)
    except Exception as ex:
        print(f"failed to start: {ex}")



if __name__ == '__main__':
    try:
        asyncio.run(if_started())
    except Exception as ex:
        print(f"FAILED: {ex}")
