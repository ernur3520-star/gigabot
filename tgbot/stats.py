# statistics related functions

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    # TODO: calculate from database
    if lang == "ru":
        text = "📊 Статистика:\n\nЗаказов сегодня: 0\nВсего заказов: 0\nВыручка: 0 тенге"
        buttons = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
        ]
    else:
        text = "📊 Статистика:\n\nБүгінгі тапсырыстар: 0\nБарлық тапсырыстар: 0\nТабыс: 0 теңге"
        buttons = [
            [InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
