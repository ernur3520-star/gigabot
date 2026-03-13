# support section

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    if lang == "ru":
        text = "🆘 Поддержка:\n\nЕсли у вас есть вопросы, проблемы или предложения — пишите напрямую: @Ironhook001. Отвечаю в течение нескольких часов 😊"
        buttons = [
            [InlineKeyboardButton("📖 Инструкция", callback_data="support_instructions")],
            [InlineKeyboardButton("❓ Частые вопросы", callback_data="support_faq")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
        ]
    else:
        text = "🆘 Қолдау:\n\nЕгер сізде сұрақтар, мәселелер немесе ұсыныстар болса — тікелей жазыңыз: @Ironhook001. Бірнеше сағат ішінде жауап беремін 😊"
        buttons = [
            [InlineKeyboardButton("📖 Нұсқаулық", callback_data="support_instructions")],
            [InlineKeyboardButton("❓ Жиі қойылатын сұрақтар", callback_data="support_faq")],
            [InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
