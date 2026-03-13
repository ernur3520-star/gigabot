import requests
from config import Settings

settings = Settings()

class WhatsAppSender:
    base_url = "https://api.green-api.com"

    @staticmethod
    def send_message(chat_id: str, text: str) -> bool:
        """Send message via Green API"""
        if not settings.green_api_instance or not settings.green_api_token:
            print("Green API credentials not configured")
            return False
        
        url = f"{WhatsAppSender.base_url}/waInstance{settings.green_api_instance}/sendMessage/{settings.green_api_token}"
        
        payload = {
            "chatId": chat_id,
            "message": text
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print(f"Message sent to {chat_id}: {text[:50]}...")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
