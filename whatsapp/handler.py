# logic to handle incoming WhatsApp messages via AI agent

from ai.agent import WhatsAppAgent
# from database.queries import save_message, insert_order
from config import Settings
import telegram
from tgbot.orders import orders_list
from whatsapp.sender import WhatsAppSender

agent = WhatsAppAgent()
settings = Settings()

agent = WhatsAppAgent()
settings = Settings()

async def handle_message(message: dict):
    """Process the JSON payload received from Green API webhook.

    Steps:
    1. parse sender number, text, attachments
    2. store raw message with save_message (not implemented yet)
    3. if user is in middle of an order flow, update state accordingly
    4. otherwise, pass message text to agent.generate_response to craft reply
    5. handle special events like receiving PDF check by invoking agent.check_payment
    6. forward commands/notifications to Telegram seller bot via queries
    """
    # Parse message
    sender = message.get("senderData", {}).get("chatId", "")
    text = message.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")
    
    if not text:
        return
    
    # Check if it's an order
    if "заказ" in text.lower() or "order" in text.lower():
        # Save order
        order_data = {
            "sender": sender,
            "text": text,
            "status": "new",
            "seller_id": settings.telegram_seller_id,  # Assuming single seller for now
            "created_at": None  # Let DB handle timestamp
        }
        # try:
        #     insert_order(order_data)
        # except Exception as e:
        #     print(f"Error saving order to DB: {e}")
        #     # Fallback to temp storage
        orders_list.append({
            "sender": sender,
            "text": text,
            "status": "new"
        })
        
        # Notify seller via Telegram
        if settings.telegram_bot_token and settings.telegram_seller_id:
            bot = telegram.Bot(token=settings.telegram_bot_token)
            await bot.send_message(
                chat_id=settings.telegram_seller_id,
                text=f"🆕 Новый заказ!\n\nОтправитель: {sender}\nТекст: {text}"
            )
    
    # Otherwise, use AI agent for response
    response = agent.generate_response(text, sender)
    # Send response back via WhatsApp
    WhatsAppSender.send_message(sender, response)
    print(f"Response: {response}")
