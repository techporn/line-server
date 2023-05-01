import logging
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError

from reply_table import ReplyTable
import line_server
import settings


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
webhook_parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
handler = line_server.Handler(line_bot_api, webhook_parser, ReplyTable())


def lambda_handler(event, context):
    # get X-Line-Signature header value
    signature = event["headers"]["x-line-signature"]

    # get request body as text
    body = event["body"]

    # handle webhook body
    try:
        return handler.handle(body, signature)
    except InvalidSignatureError as err:
        return err


if __name__ == "__main__":
    pass
