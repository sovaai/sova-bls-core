from dp_client.client import Client
import logging
import config
import datetime


class DialogCore:

    host = config.NLAB_SOVA_ENGINE_HOST

    def __init__(self, message: dict):
        self.message = message
        logging.debug(f"Инициализировали диалог {self.message}")
        self.dp_client = Client(connection_string=config.NLAB_SOVA_ENGINE_HOST)

    async def send_request(self):
        try:
            logging.debug(
                f"request: {self.message['text']}"
                f" session_id: {self.message['technical_info']['session_id']}"
                f" session_context: {dict()}"
                f" bot_id: {self.message['technical_info']['inf_id']}"
                f" bot_context: {dict()}"
            )
            resp = self.dp_client.easy_request(
                request=self.message['text'],
                session_id=self.message['technical_info']['session_id'],
                session_context={},
                bot_id=self.message['technical_info']['inf_id'],
                bot_context={
                    "inf_person": self.message['technical_info']['inf_profile'],
                    "inf_name": '',
                }
            )
            logging.debug(f"resp : {resp} text : {resp['text']}")
            self.message['response'] = resp
            self.message['technical_info'].update({
                "resp_ts": datetime.datetime.now(),
                'response': resp['text'],
                'resp_cntx': resp['vars'],
            })

        except Exception as err:
            self.message['error'] = f"Dialog send error without init {err.__str__()} resp {resp}"
            return self

    async def send_event(self):
        """

        :return:
        """
        try:
            resp = self.dp_client.easy_request(
                request=self.message['euid'],
                session_id=self.message['technical_info']['session_id'],
                session_context={},
                bot_id=self.message['technical_info']['inf_id'],
                bot_context={
                    "inf_person": self.message['technical_info']['inf_profile'],
                    "inf_name": '',
                }
            )
            self.message['response'] = resp
            self.message['technical_info'].update({
                "resp_ts": datetime.datetime.now(),
                'response': resp['text'],
                'resp_cntx': resp['vars'],
            })

        except Exception as err:
            self.message['error'] = f"Dialog send error {err.__str__()}"
            return self

    async def process(self):
        if self.message['type'] == 'request':
            await self.send_request()
        elif self.message['type'] == 'event':
            await self.send_event()