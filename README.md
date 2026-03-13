# Gigabot

Система для продажи интернет-пакетов (гигабайт) в Казахстане.

## Описание

Проект состоит из двух подсистем:

1. **WhatsApp агент** для общения с клиентами, реализованный на FastAPI и Green API. Агент ведёт себя как живой продавец.
2. **Telegram бот** для продавцов, которые регистрируются, управляют заказами и получают уведомления.

Система использует Supabase для хранения данных, Gemini 1.5 Flash для ИИ и проверки чеков, а также Railway для хостинга.

## Технологии

- Python 3.11+
- FastAPI
- Supabase (Postgres)
- Green API (WhatsApp)
- python-telegram-bot
- Gemini 1.5 Flash (Google generative AI)
- Railway (развертывание)

## Развертывание на Railway

### Шаг 1: Подготовка
1. Создайте аккаунт на [Railway.app](https://railway.app)
2. Установите Railway CLI: `npm install -g @railway/cli`
3. Авторизуйтесь: `railway login`

### Шаг 2: Настройка переменных окружения
В Railway dashboard или через CLI установите следующие переменные:

```bash
# WhatsApp (Green API)
railway variables set GREEN_API_INSTANCE=7107545439
railway variables set GREEN_API_TOKEN=ваш_green_api_token

# Telegram Bot
railway variables set TELEGRAM_BOT_TOKEN=ваш_telegram_bot_token

# Gemini AI
railway variables set GEMINI_API_KEY=ваш_gemini_api_key

# Supabase Database
railway variables set SUPABASE_URL=https://ваш.supabase.url
railway variables set SUPABASE_KEY=ваш_supabase_key

# Billing
railway variables set SUBSCRIPTION_CARD=номер_карты_kaspi
railway variables set SUBSCRIPTION_PRICE=500
railway variables set TRIAL_DAYS=7

# Admin
railway variables set TELEGRAM_SELLER_ID=ваш_telegram_chat_id
```

### Шаг 3: Развертывание
```bash
# Создайте новый проект
railway init gigabot

# Перейдите в директорию проекта
cd gigabot

# Разверните
railway up
```

### Шаг 4: Настройка вебхуков
После развертывания:
1. Получите URL вашего Railway приложения
2. Настройте вебхук в Green API: `https://ваш-railway-url.railway.app/whatsapp/webhook`
3. Убедитесь, что Telegram бот токен действующий

## Локальный запуск

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите систему
python run.py
```

4. **Проверьте логи**:
   ```bash
   railway logs
   ```

## Локальный запуск

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите сервер
python run.py
```

## Использование

- Клиенты пишут в WhatsApp на номер продавца
- ИИ агент отвечает и продаёт пакеты
- Продавцы управляют системой через Telegram бот

## Структура проекта

```
gigabot/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── whatsapp/
│   ├── webhook.py
│   ├── sender.py
│   ├── handler.py
│   └── green_api.py
├── tgbot/
│   ├── bot.py
│   ├── menu.py
│   ├── orders.py
│   ├── stats.py
│   ├── packages.py
│   ├── settings.py
│   ├── subscription.py
│   ├── registration.py
│   └── support.py
├── ai/
│   ├── agent.py
│   ├── payment_check.py
│   └── prompts.py
└── database/
    ├── models.py
    ├── queries.py
    └── supabase.py
```

## Запуск

```bash
pip install -r requirements.txt
uvicorn gigabot.main:app --reload
```

Далее необходимо заполнить `.env` и завершить реализацию модулей.
