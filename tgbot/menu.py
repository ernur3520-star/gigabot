from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("Қазақша", callback_data="lang_kz")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите язык:", reply_markup=reply_markup)


async def show_registration_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str = "ru"):
    if language == "ru":
        text = "👋 Добро пожаловать!\n\nДля начала работы нужно зарегистрироваться.\n\nНажмите 'Начать регистрацию' для продолжения."
        buttons = [[InlineKeyboardButton("📝 Начать регистрацию", callback_data="reg_start")]]
    else:
        text = "👋 Қош келдіңіз!\n\nЖұмысты бастау үшін тіркелу қажет.\n\nЖалғастыру үшін 'Тіркеуді бастау' түймесін басыңыз."
        buttons = [[InlineKeyboardButton("📝 Тіркеуді бастау", callback_data="reg_start")]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str = "ru"):
    # Check subscription
    from datetime import datetime, timedelta
    registered_at = context.user_data.get("registered_at")
    if registered_at:
        trial_end = registered_at + timedelta(days=7)
        if datetime.now() > trial_end and not context.user_data.get("subscription_paid", False):
            await show_subscription_menu(update, context, language)
            return
    
    name = context.user_data.get("name", "Продавец")
    subscription_status = "Пробный период" if not context.user_data.get("subscription_paid", False) else "Подписка активна"
    
    if language == "ru":
        text = f"👋 {name}\n\nСтатус: {subscription_status}\nНовых заказов: 0\n\nГлавное меню:"
        buttons = [
            [InlineKeyboardButton("🆕 Новые заказы", callback_data="menu_orders_new")],
            [InlineKeyboardButton("📋 Все заказы", callback_data="menu_orders_all")],
            [InlineKeyboardButton("📊 Статистика", callback_data="menu_stats")],
            [InlineKeyboardButton("💰 Мой заработок", callback_data="menu_earnings")],
            [InlineKeyboardButton("📦 Мои пакеты", callback_data="menu_packages")],
            [InlineKeyboardButton("⚙️ Настройки", callback_data="menu_settings")],
            [InlineKeyboardButton("💳 Подписка", callback_data="menu_subscription")],
            [InlineKeyboardButton("🆘 Поддержка", callback_data="menu_support")],
            [InlineKeyboardButton("🔄 Обновить", callback_data="menu_refresh")],
        ]
    else:  # kz
        text = f"👋 {name}\n\nМәртебе: {subscription_status}\nЖаңа тапсырыстар: 0\n\nНегізгі мәзір:"
        buttons = [
            [InlineKeyboardButton("🆕 Жаңа тапсырыстар", callback_data="menu_orders_new")],
            [InlineKeyboardButton("📋 Барлық тапсырыстар", callback_data="menu_orders_all")],
            [InlineKeyboardButton("📊 Статистика", callback_data="menu_stats")],
            [InlineKeyboardButton("💰 Менің табысым", callback_data="menu_earnings")],
            [InlineKeyboardButton("📦 Менің пакеттерім", callback_data="menu_packages")],
            [InlineKeyboardButton("⚙️ Параметрлер", callback_data="menu_settings")],
            [InlineKeyboardButton("💳 Жазылым", callback_data="menu_subscription")],
            [InlineKeyboardButton("🆘 Қолдау", callback_data="menu_support")],
            [InlineKeyboardButton("🔄 Жаңарту", callback_data="menu_refresh")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)


async def show_subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str = "ru"):
    if language == "ru":
        text = "Ваш бесплатный период истек. Для продолжения работы оплатите подписку: 500 тенге на Kaspi.\n\nРеквизиты: [номер карты из config]\n\nПосле оплаты отправьте чек (фото) для активации."
        buttons = [
            [InlineKeyboardButton("💳 Я оплатил - отправить чек", callback_data="sub_pay")],
            [InlineKeyboardButton("📞 Поддержка", callback_data="menu_support")],
        ]
    else:
        text = "Сіздің тегін кезеңі аяқталды. Жұмысты жалғастыру үшін жазылымды төлеңіз: 500 теңге Kaspi-де.\n\nРеквизиттер: [карта нөмірі config-тен]\n\nТөлемнен кейін чекті (фото) жіберіңіз активация үшін."
        buttons = [
            [InlineKeyboardButton("💳 Мен төледім - чек жіберу", callback_data="sub_pay")],
            [InlineKeyboardButton("📞 Қолдау", callback_data="menu_support")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)


async def show_earnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    # TODO: calculate earnings from database
    if lang == "ru":
        text = "💰 Мой заработок:\n\nСегодня: 0 тг\nЗа неделю: 0 тг\nЗа месяц: 0 тг\n\nИстория продаж:\n(Здесь будет список продаж)"
        buttons = [[InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")]]
    else:
        text = "💰 Менің табысым:\n\nБүгін: 0 теңге\nАптада: 0 теңге\nАйда: 0 теңге\n\nСатылым тарихы:\n(Мұнда сатылым тізімі болады)"
        buttons = [[InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

async def show_packages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    # TODO: load packages from database
    packages = [
        {"operator": "Kcell", "gb": 5, "price": 500, "active": True},
        {"operator": "Beeline", "gb": 10, "price": 1000, "active": True},
    ]
    
    if lang == "ru":
        text = "📦 Мои пакеты:\n\n"
        for pkg in packages:
            status = "✅ Включен" if pkg["active"] else "❌ Выключен"
            text += f"{pkg['operator']}: {pkg['gb']}ГБ - {pkg['price']}тг ({status})\n"
        buttons = [
            [InlineKeyboardButton("➕ Добавить пакет", callback_data="packages_add")],
            [InlineKeyboardButton("✏️ Изменить цену", callback_data="packages_edit")],
            [InlineKeyboardButton("🗑️ Удалить пакет", callback_data="packages_delete")],
            [InlineKeyboardButton("🔄 Вкл/Выкл", callback_data="packages_toggle")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
        ]
    else:
        text = "📦 Менің пакеттерім:\n\n"
        for pkg in packages:
            status = "✅ Қосулы" if pkg["active"] else "❌ Өшірулі"
            text += f"{pkg['operator']}: {pkg['gb']}ГБ - {pkg['price']}теңге ({status})\n"
        buttons = [
            [InlineKeyboardButton("➕ Пакет қосу", callback_data="packages_add")],
            [InlineKeyboardButton("✏️ Бағаны өзгерту", callback_data="packages_edit")],
            [InlineKeyboardButton("🗑️ Пакет жою", callback_data="packages_delete")],
            [InlineKeyboardButton("🔄 Қосу/Өшіру", callback_data="packages_toggle")],
            [InlineKeyboardButton("⬅️ Артқа", callback_data="menu_back")],
        ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
