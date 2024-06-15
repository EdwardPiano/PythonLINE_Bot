from typing import Text
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from models.message_request import MessageRequest

from linebot.v3.messaging import (
    TextMessage,
)
from skills import add_skill


@add_skill("name")
def get(message_request: MessageRequest):
    return [TextMessage(text="Edward")]
