import logging
from kernel.tools import FindOverAllExtensions


class PreProcessor:
    """
        Предварительная обработка сообщений
    """
    external_modules = FindOverAllExtensions('preprocessor').run()

    def __init__(self, message: dict):
        self.message = message
        logging.debug(f"Preprocessing of messages {message} id {id(message)} external_modules {self.external_modules}")

    async def process(self):
        for m in self.external_modules:
            await m.main(self.message)
