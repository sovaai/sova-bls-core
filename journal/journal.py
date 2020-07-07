from kernel.tools import FindOverAllExtensions


class Journal:

    external_modules = FindOverAllExtensions('journal').run()

    def __init__(self, message: dict):
        self.message = message

    async def process(self):
        for m in self.external_modules:
            await m.main(self.message)
