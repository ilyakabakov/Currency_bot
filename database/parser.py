import asyncio



import json

import requests

from database.config import URL, FILE_NAME


class CurrencyParser:
    def __init__(self):
        self.url = URL
        self.file_name = FILE_NAME
        self.data = None

    async def update_data(self):
        request = requests.get(url=self.url)
        if request.status_code == 200:
            self.data = request.json()
            with open(self.file_name, 'w') as file:
                json.dump(self.data, file)
            print(f'Successfully updated data at {self.file_name}')
        else:
            print(f'Failed to update data. Server status code: {request.status_code}')

    async def get_data(self, query, currency):
        if self.data is None:
            await self.update_data()

        return self.data[query][currency]['Value']

    async def get_data_json(self, query):
        if self.data is None:
            await self.update_data()

        return self.data.get(query)


async def main():
    parser = CurrencyParser()

    # Обновляем данные каждые полчаса
    while True:
        await parser.update_data()
        await asyncio.sleep(1800)  # 1800 секунд = 30 минут
