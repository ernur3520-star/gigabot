import os
import sys
from datetime import datetime

# When running this file directly (e.g. `py tgbot/bot.py`), ensure the project root
# is on sys.path so shared modules (like config) can be imported.
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import Settings
from tgbot import menu
from tgbot import orders
from tgbot import stats
from tgbot import settings
from tgbot import support
# from database import queries
from ai.payment_check import check_payment  # TODO: implement

settings: Settings | None
try:
    settings = Settings()
except Exception as e:
    # Avoid crash when `.env` is missing or invalid; print guidance instead.
    print("ERROR: failed to load settings (check your .env file):", e)
    settings = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Load from database
    # try:
    #     result = queries.get_seller_by_telegram_id(user_id)
    #     if result.data:
    #         seller = result.data[0]
    #         context.user_data.update({
    #             "registered": True,
    #             "name": seller.get("name"),
    #             "phone": seller.get("phone"),
    #             "language": seller.get("language", "ru"),
    #             "registered_at": seller.get("registered_at"),
    #             "subscription_paid": seller.get("subscription_paid", False),
    #         })
    # except Exception as e:
    #     print(f"Error loading seller data: {e}")
    
    registered = context.user_data.get("registered", False)
    
    if registered:
        # Check subscription
        from datetime import datetime, timedelta
        registered_at = context.user_data.get("registered_at")
        if registered_at:
            if isinstance(registered_at, str):
                registered_at = datetime.fromisoformat(registered_at.replace('Z', '+00:00'))
            trial_end = registered_at + timedelta(days=7)
            if datetime.now() > trial_end and not context.user_data.get("subscription_paid", False):
                await menu.show_subscription_menu(update, context, context.user_data.get("language", "ru"))
                return
        
        # Show language selection or main menu if language already set
        lang = context.user_data.get("language")
        if lang:
            await menu.show_main_menu(update, context, lang)
        else:
            await menu.show_language_selection(update, context)
    else:
        # For new users, ask language first if not set
        lang = context.user_data.get("language")
        if lang:
            await menu.show_registration_prompt(update, context, lang)
        else:
            await menu.show_language_selection(update, context)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lang_ru":
        context.user_data["language"] = "ru"
        if context.user_data.get("registered", False):
            await menu.show_main_menu(update, context, "ru")
        else:
            await menu.show_registration_prompt(update, context, "ru")
    elif query.data == "lang_kz":
        context.user_data["language"] = "kz"
        if context.user_data.get("registered", False):
            await menu.show_main_menu(update, context, "kz")
        else:
            await menu.show_registration_prompt(update, context, "kz")
    elif query.data == "reg_start":
        context.user_data["reg_step"] = "name"
        lang = context.user_data.get("language", "ru")
        if lang == "ru":
            await query.edit_message_text("Введите ваше имя:")
        else:
            await query.edit_message_text("Атыңызды енгізіңіз:")
    elif query.data == "sub_pay":
        context.user_data["waiting_for_check"] = True
        lang = context.user_data.get("language", "ru")
        if lang == "ru":
            await query.edit_message_text("Отправьте фото чека оплаты (скриншот из Kaspi). После проверки подписка будет активирована.")
        else:
            await query.edit_message_text("Төлем чегінің фотосын жіберіңіз (Kaspi-ден скриншот). Тексеруден кейін жазылым белсендіріледі.")
    elif query.data.startswith("menu_"):
        if query.data == "menu_orders_new":
            await orders.show_new_orders(update, context)
        elif query.data == "menu_orders_all":
            await orders.show_all_orders(update, context)
        elif query.data == "menu_stats":
            await stats.show_statistics(update, context)
        elif query.data == "menu_earnings":
            await menu.show_earnings(update, context)
        elif query.data == "menu_packages":
            await menu.show_packages(update, context)
        elif query.data == "menu_subscription":
            await menu.show_subscription_menu(update, context, context.user_data.get("language", "ru"))
        elif query.data == "menu_refresh":
            lang = context.user_data.get("language", "ru")
            await menu.show_main_menu(update, context, lang)
        elif query.data == "menu_back":
            lang = context.user_data.get("language", "ru")
            await menu.show_main_menu(update, context, lang)
        elif query.data == "menu_settings":
            await settings.show_settings(update, context)
        elif query.data == "settings_name":
            context.user_data["changing"] = "name"
            lang = context.user_data.get("language", "ru")
            if lang == "ru":
                await query.edit_message_text("Введите новое имя:")
            else:
                await query.edit_message_text("Жаңа атыңызды енгізіңіз:")
        elif query.data == "settings_phone":
            context.user_data["changing"] = "phone"
            lang = context.user_data.get("language", "ru")
            if lang == "ru":
                await query.edit_message_text("Введите новый номер телефона:")
            else:
                await query.edit_message_text("Жаңа телефон нөміріңізді енгізіңіз:")
        elif query.data.startswith("settings_"):
            if query.data == "settings_whatsapp":
                context.user_data["changing"] = "whatsapp"
                lang = context.user_data.get("language", "ru")
                await query.edit_message_text("Введите новый WhatsApp номер:" if lang == "ru" else "Жаңа WhatsApp нөмірін енгізіңіз:")
            elif query.data == "settings_kaspi":
                context.user_data["changing"] = "kaspi"
                lang = context.user_data.get("language", "ru")
                await query.edit_message_text("Введите новый номер Kaspi карты:" if lang == "ru" else "Жаңа Kaspi карта нөмірін енгізіңіз:")
            else:
                lang = context.user_data.get("language", "ru")
                await query.edit_message_text("Функция в разработке." if lang == "ru" else "Функция әзірленуде.")
        elif query.data == "menu_support":
            await support.show_support(update, context)
        elif query.data == "support_instructions":
            lang = context.user_data.get("language", "ru")
            text = "📖 Инструкция:\n\n(Здесь будет подробная инструкция по использованию системы)" if lang == "ru" else "📖 Нұсқаулық:\n\n(Мұнда жүйені пайдалану бойынша толық нұсқаулық болады)"
            buttons = [[InlineKeyboardButton("⬅️ Назад" if lang == "ru" else "⬅️ Артқа", callback_data="menu_support")]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text, reply_markup=reply_markup)
        elif query.data == "support_faq":
            lang = context.user_data.get("language", "ru")
            text = "❓ Частые вопросы:\n\n(Здесь будут ответы на часто задаваемые вопросы)" if lang == "ru" else "❓ Жиі қойылатын сұрақтар:\n\n(Мұнда жиі қойылатын сұрақтарға жауаптар болады)"
            buttons = [[InlineKeyboardButton("⬅️ Назад" if lang == "ru" else "⬅️ Артқа", callback_data="menu_support")]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.edit_message_text(text, reply_markup=reply_markup)
        elif query.data.startswith("packages_"):
            lang = context.user_data.get("language", "ru")
            await query.edit_message_text("Функция в разработке." if lang == "ru" else "Функция әзірленуде.")
            await support.show_support(update, context)
        elif query.data == "menu_back":
            lang = context.user_data.get("language", "ru")
            await menu.show_main_menu(update, context, lang)
        else:
            lang = context.user_data.get("language", "ru")
            if lang == "ru":
                await query.edit_message_text("Функция в разработке.")
            else:
                await query.edit_message_text("Функция әзірленуде.")
    else:
        lang = context.user_data.get("language", "ru")
        if lang == "ru":
            await query.edit_message_text("Неизвестная команда. Попробуйте /start")
        else:
            await query.edit_message_text("Белгісіз команда. /start көріңіз")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("reg_step")
    waiting_check = context.user_data.get("waiting_for_check", False)
    changing = context.user_data.get("changing")
    
    if changing:
        text = update.message.text
        lang = context.user_data.get("language", "ru")
        updates = {}
        if changing == "name":
            context.user_data["name"] = text
            updates["name"] = text
            if lang == "ru":
                reply_text = f"Имя изменено на: {text}"
            else:
                reply_text = f"Аты өзгертілді: {text}"
        elif changing == "phone":
            context.user_data["phone"] = text
            updates["phone"] = text
            if lang == "ru":
                reply_text = f"Телефон изменен на: {text}"
            else:
                reply_text = f"Телефон өзгертілді: {text}"
        elif changing == "whatsapp":
            context.user_data["whatsapp"] = text
            updates["whatsapp"] = text
            if lang == "ru":
                reply_text = f"WhatsApp изменен на: {text}"
            else:
                reply_text = f"WhatsApp өзгертілді: {text}"
        elif changing == "kaspi":
            context.user_data["kaspi"] = text
            updates["kaspi"] = text
            if lang == "ru":
                reply_text = f"Kaspi карта изменена на: {text}"
            else:
                reply_text = f"Kaspi карта өзгертілді: {text}"
        context.user_data.pop("changing", None)
        # Update database
        # try:
        #     queries.update_seller(update.effective_user.id, updates)
        # except Exception as e:
        #     print(f"Error updating seller: {e}")
        # Show updated settings with menu
        name = context.user_data.get("name", "Не указано")
        phone = context.user_data.get("phone", "Не указано")
        if lang == "ru":
            text_full = f"⚙️ Настройки:\n\nИмя: {name}\nТелефон: {phone}\n\n{reply_text}"
            buttons = [
                [InlineKeyboardButton("Изменить имя", callback_data="settings_name")],
                [InlineKeyboardButton("Изменить телефон", callback_data="settings_phone")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
            ]
        else:
            text_full = f"⚙️ Параметрлер:\n\nАты: {name}\nТелефон: {phone}\n\n{reply_text}"
            buttons = [
                [InlineKeyboardButton("Атын өзгерту", callback_data="settings_name")],
                [InlineKeyboardButton("Телефонды өзгерту", callback_data="settings_phone")],
                [InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")],
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(text_full, reply_markup=reply_markup)
        return
    
    if waiting_check and update.message.photo:
        # TODO: download and check photo
        # For now, simulate success
        context.user_data["subscription_paid"] = True
        context.user_data["waiting_for_check"] = False
        # Update database
        # try:
        #     queries.update_seller(update.effective_user.id, {"subscription_paid": True})
        # except Exception as e:
        #     print(f"Error updating subscription: {e}")
        lang = context.user_data.get("language", "ru")
        if lang == "ru":
            text = "Чек проверен! Подписка активирована. Добро пожаловать в меню."
        else:
            text = "Чек тексерілді! Жазылым белсендірілді. Мәзірге қош келдіңіз."
        # Show main menu with buttons
        buttons = [
            [InlineKeyboardButton("🆕 Новые заказы" if lang == "ru" else "🆕 Жаңа тапсырыстар", callback_data="menu_orders_new")],
            [InlineKeyboardButton("📋 Все заказы" if lang == "ru" else "📋 Барлық тапсырыстар", callback_data="menu_orders_all")],
            [InlineKeyboardButton("📊 Статистика", callback_data="menu_stats")],
            [InlineKeyboardButton("⚙️ Настройки" if lang == "ru" else "⚙️ Параметрлер", callback_data="menu_settings")],
            [InlineKeyboardButton("🆘 Поддержка" if lang == "ru" else "🆘 Қолдау", callback_data="menu_support")],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return
    
    if not step:
        return  # Not in registration
    
    text = update.message.text
    lang = context.user_data.get("language", "ru")
    
    if step == "name":
        context.user_data["name"] = text
        context.user_data["reg_step"] = "phone"
        if lang == "ru":
            await update.message.reply_text("Введите ваш номер телефона:")
        else:
            await update.message.reply_text("Телефон нөміріңізді енгізіңіз:")
    elif step == "phone":
        context.user_data["phone"] = text
        # Save to database
        # seller_data = {
        #     "telegram_id": update.effective_user.id,
        #     "name": context.user_data["name"],
        #     "phone": text,
        #     "language": context.user_data.get("language", "ru"),
        #     "registered_at": datetime.now().isoformat(),
        #     "subscription_paid": False,
        # }
        # try:
        #     queries.insert_seller(seller_data)
        # except Exception as e:
        #     print(f"Error saving seller: {e)")
        context.user_data["registered"] = True
        context.user_data["registered_at"] = datetime.now()
        context.user_data.pop("reg_step", None)
        if lang == "ru":
            text = "Регистрация завершена! Добро пожаловать."
        else:
            text = "Тіркелу аяқталды! Қош келдіңіз."
        # Show main menu with buttons
        buttons = [
            [InlineKeyboardButton("🆕 Новые заказы" if lang == "ru" else "🆕 Жаңа тапсырыстар", callback_data="menu_orders_new")],
            [InlineKeyboardButton("📋 Все заказы" if lang == "ru" else "📋 Барлық тапсырыстар", callback_data="menu_orders_all")],
            [InlineKeyboardButton("📊 Статистика", callback_data="menu_stats")],
            [InlineKeyboardButton("⚙️ Настройки" if lang == "ru" else "⚙️ Параметрлер", callback_data="menu_settings")],
            [InlineKeyboardButton("🆘 Поддержка" if lang == "ru" else "🆘 Қолдау", callback_data="menu_support")],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(text, reply_markup=reply_markup)


def run_bot():
    if not settings:
        print("ERROR: failed to load settings")
        return

    token = getattr(settings, "telegram_bot_token", None)
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set")
        return

    try:
        app = ApplicationBuilder().token(token).build()
    except Exception as e:
        print(f"ERROR: failed to build Telegram application: {e}")
        return

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot starting...")
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e:
        print(f"ERROR: Bot polling failed: {e}")
        return


if __name__ == "__main__":
    run_bot()
