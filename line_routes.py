from fastapi import APIRouter, Request, Header
from line_handlers import handle_line_webhook

line_router = APIRouter()


@line_router.post("/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    await handle_line_webhook(request, x_line_signature)
    return {}
