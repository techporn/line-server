import boto3
from boto3.dynamodb.conditions import Key, Attr

import settings


class ReplyTable:
    def __init__(self):
        self.__dynamodb = boto3.resource(
            "dynamodb",
            region_name=settings.DYNAMODB_REGION,
            endpoint_url=settings.DYNAMODB_ENDPOINT,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.table = self.__dynamodb.Table(settings.DYNAMODB_TABLE)

    def get_responses(self, text):
        scenario = self.table.get_item(
            Key={"text": text}, ProjectionExpression="responses"
        )
        return scenario.get("Item", {}).get("responses", [])

    def get_item(self, **args):
        return {"Item": {"responses": [{"type": "text", "text": "dummy"}]}}
