import asyncio
import logging
import random

from nextion import Nextion, EventType


class App:
    def __init__(self):
        self.client = Nextion('COM29', 115200, self.event_handler)

    async def event_handler(self, type_, data):
        if type_ == EventType.STARTUP:
            print('We have booted up!')
        elif type_ == EventType.TOUCH:
            print('A button (id: %d) was touched on page %d' % (data.component_id, data.page_id))

        logging.info('Event %s data: %s', type, str(data))

        print(await self.client.get('gear.txt'))

    async def run(self):
        await self.client.connect()

        print(await self.client.get('gear.txt'))

        await self.client.set('gear.txt', F"1")


class DisplayViewModel:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
            handlers=[
                logging.StreamHandler()
            ])
        loop = asyncio.get_event_loop()
        self.app = App()
        asyncio.ensure_future(self.app.run())
        loop.run_forever()
