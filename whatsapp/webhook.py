from fastapi import APIRouter, Request
from whatsapp.handler import handle_message

router = APIRouter()

@router.post("/whatsapp/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    # Process messages
    messages = payload.get("messages", [])
    for msg in messages:
        await handle_message(msg)
    return {"status": "ok"}
