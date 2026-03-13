# seller settings

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    name = context.user_data.get("name", "Не указано")
    phone = context.user_data.get("phone", "Не указано")
    whatsapp = context.user_data.get("whatsapp", "Не подключен")
    kaspi = context.user_data.get("kaspi", "Не указана")
    
    if lang == "ru":
        text = f"⚙️ Настройки:\n\nИмя: {name}\nWhatsApp: {whatsapp}\nKaspi карта: {kaspi}"
        buttons = [
            [InlineKeyboardButton("Изменить имя", callback_data="settings_name")],
            [InlineKeyboardButton("Изменить WhatsApp номер", callback_data="settings_whatsapp")],
            [InlineKeyboardButton("Переподключить WhatsApp", callback_data="settings_reconnect_whatsapp")],
            [InlineKeyboardButton("Изменить Kaspi карту", callback_data="settings_kaspi")],
            [InlineKeyboardButton("Изменить операторы", callback_data="settings_operators")],
            [InlineKeyboardButton("🔔 Уведомления вкл/выкл", callback_data="settings_notifications")],
            [InlineKeyboardButton("⏸️ Режим паузы", callback_data="settings_pause")],
            [InlineKeyboardButton("🌐 Сменить язык", callback_data="settings_language")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
        ]
    else:
        text = f"⚙️ Параметрлер:\n\nАты: {name}\nWhatsApp: {whatsapp}\nKaspi карта: {kaspi}"
        buttons = [
            [InlineKeyboardButton("Атын өзгерту", callback_data="settings_name")],
            [InlineKeyboardButton("WhatsApp нөмірін өзгерту", callback_data="settings_whatsapp")],
            [InlineKeyboardButton("WhatsApp қайта қосу", callback_data="settings_reconnect_whatsapp")],
            [InlineKeyboardButton("Kaspi картаны өзгерту", callback_data="settings_kaspi")],
            [InlineKeyboardButton("Операторларды өзгерту", callback_data="settings_operators")],
            [InlineKeyboardButton("🔔 Хабарландырулар қосу/өшіру", callback_data="settings_notifications")],
            [InlineKeyboardButton("⏸️ Кідіріс режимі", callback_data="settings_pause")],
            [InlineKeyboardButton("🌐 Тілді өзгерту", callback_data="settings_language")],
            [InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
