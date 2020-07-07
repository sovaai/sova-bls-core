import logging
from kernel.context import ContextCore
from kernel.journal import Journal
from kernel.preprocessor import PreProcessor
from kernel.postprocessor import PostProcessor
from kernel.dialog import DialogCore


class MessageHandler:
    """
        Основной класс обработки сообщений.
    """

    status_code = 200

    def __init__(self, message: dict):
        self.message = message
        logging.debug(f"Пришли в обработчик сообщений {self.message} id {id(self.message)}")

    async def process(self):

        context = ContextCore(self.message)
        await context.process()
        if self.message.get("error"):
            self.status_code = 400
            return self.message

        preprocessor = PreProcessor(self.message)
        await preprocessor.process()
        if self.message.get("error"):
            self.status_code = 400
            return self.message

        if not self.message['technical_info'].get('not_send_engine'):
            dialog = DialogCore(self.message)
            await dialog.process()
            if self.message.get("error"):
                self.status_code = 400
                return self.message
        else:
            logging.debug("Не отправляем запрос")

        postprocess = PostProcessor(self.message)
        await postprocess.process()
        if self.message.get("error"):
            self.status_code = 400
            return self.message

        journal = Journal(self.message)
        await journal.process()
        if self.message.get("error"):
            self.status_code = 400
            return self.message

        await context.store(message=self.message)
        return self.message
