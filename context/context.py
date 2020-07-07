import logging
from kernel.tools import FindOverAllExtensions


class ContextCore:

    external_extensions = FindOverAllExtensions('context').run()
    store_extensions = FindOverAllExtensions('context.store').get_store_extension()

    def __init__(self, message: dict):
        logging.debug(f"Context init {message} external_modules {self.external_extensions}")
        self.message = message

    async def process(self):
        for m in self.external_extensions:
            await m.main(self.message)
        return self.message

    async def store(self, message: dict):
        logging.debug(f"Store extensions {self.store_extensions}")
        for m in self.store_extensions:
            await m.store(message)
        return self.message
