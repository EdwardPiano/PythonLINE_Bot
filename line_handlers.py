import os
import re
import logging
from dotenv import load_dotenv
from models.message_request import MessageRequest
from fastapi import Request, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from skills import *
from skills import skills

load_dotenv()

# 初始化日志
logging.basicConfig(level=logging.INFO)

# 初始化 LINE Bot API 和 Webhook Handler
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def get_message(request: MessageRequest):
    for pattern, skill in skills.items():
        logging.info(f"pattern: {pattern}")
        logging.info(f"request.intent: {request.intent}")
        logging.info(f"skills : {skills}")
        logging.info(f"skill : {skill}")
        if re.match(pattern, request.intent, re.IGNORECASE):
            return skill(request)
    return skills["{not_match}"](request)


async def handle_line_webhook(request: Request, x_line_signature: str):
    body = await request.body()
    logging.info(f"x-line-signature: {x_line_signature}")
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        logging.error("Invalid Signature")
        raise HTTPException(
            status_code=400, detail="Invalid Signature check your channel secret"
        )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg_request = MessageRequest(
        user_id=event.source.user_id,
        intent=event.message.text,
        message=event.message.text,
    )

    func = get_message(msg_request)
    logging.info(msg_request)

    # line_bot_api.reply_message(event.reply_token, func)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=func,
            )
        )
