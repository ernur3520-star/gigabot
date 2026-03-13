# AI agent logic for WhatsApp conversation and payment checking

import google.genai as genai
from config import Settings

settings = Settings()

class WhatsAppAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        # Load packages from database or config
        self.packages = self.load_packages()
        self.kaspi_card = settings.subscription_card or "7476734610"

    def load_packages(self):
        # TODO: load from database
        return [
            {"operator": "Kcell", "gb": 5, "price": 500},
            {"operator": "Beeline", "gb": 10, "price": 1000},
            {"operator": "Tele2", "gb": 15, "price": 1500},
        ]

    def generate_response(self, message: str, sender: str = ""):
        """Generate response using Gemini with system prompt"""
        system_prompt = f"""Ты продавец интернет-пакетов в Казахстане. Общаешься коротко и дружелюбно как живой человек. Никогда не говори что ты ИИ или бот. Если спрашивают "ты бот?" отвечай "Нет, всё в порядке 😄 Чем помочь?"

Пакеты: {self.packages}
Kaspi карта: {self.kaspi_card}

Правила:
- Определяй язык клиента и отвечай на нём
- Показывай пакеты когда просят купить ГБ
- Проси оплатить на Kaspi карту
- После получения чека говори "Получил, всё хорошо ✅ Сейчас отправлю, подождите пару минут ⏳"
- Помни предыдущие покупки клиента"""

        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"{system_prompt}\n\nСообщение клиента: {message}"
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini error: {e}")
            return "Извините, технические неполадки. Попробуйте позже."
