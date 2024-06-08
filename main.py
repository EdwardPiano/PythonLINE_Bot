import os
from dotenv.main import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException

# from fastapi.params import Header
from linebot.api import LineBotApi
from linebot.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = FastAPI()

load_dotenv()

# 初始化
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.post("/api/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400, detail="Invalid Signature check you channel secret"
        )
    return


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event):
    msg = TextSendMessage(text=f"yougyugyug said : {event.message.text}")
    line_bot_api.reply_message(event.reply_token, msg)
