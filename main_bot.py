import logging
import os

from aiogram.utils import executor

from initialize import dp

cwd = os.getcwd()

logging.basicConfig(filename=os.path.join(cwd, 'logs/main.log'))

async def if_started():

    print('Bot is ONLINE')


async def on_startup(dp):
    await if_started()

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True,
                               on_startup=on_startup
                               #on_shutdown=on_shutdown
                                )

    except Exception as ex:
        print(f"FAILED: {ex}")
