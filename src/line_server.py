from linebot.models import MessageEvent, TextSendMessage, FlexSendMessage

import logging


class Handler:
    def __init__(self, line_bot_api, parser, table):
        self.line_bot_api = line_bot_api
        self.parser = parser
        self.table = table

    def handle(self, body, signature):
        events = self.parser.parse(body, signature)
        self._handle_events(events)

    def _handle_events(self, events):
        for event in events:
            if isinstance(event, MessageEvent):
                logging.info(f"MessageEvent")
                message = event.message
                responses = self.table.get_responses(message)
            else:
                pass

            if responses:
                self.reply(event, responses)

    def reply(self, event, responses):
        logging.info(f"リプライ実行")

        for response in responses:
            type = response.get("type", "").lower()
            logging.info(f"type: {type}")

            if type == "rm":
                self.set_user_richmenu(response.get("contents"))
            elif type == "text":
                message = TextSendMessage(response.get("text"))
                self.line_bot_api.reply_message(event.reply_token, message)
            elif type == "flex":
                message = FlexSendMessage(
                    alt_text=response["alt_text"], contents=response["contents"]
                )
                self.line_bot_api.reply_message(event.reply_token, message)
            else:
                logging.WARNING(f"no match")

    def set_user_richmenu(self, menuid):
        pass


if __name__ == "__main__":
    pass


"""
a, [id1, id2]
or
a, message, hello
b, menu, {}
---
id1, message, hello
id2, message, world
"""
