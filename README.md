# 🚀 Быстрое развертывание Gigabot

## ⚡ 5-минутное развертывание

### Шаг 1: Создайте GitHub репозиторий
1. Перейдите на [github.com/new](https://github.com/new)
2. **Repository name:** `gigabot`
3. **Public** репозиторий
4. **НЕ** добавляйте README, .gitignore, лицензию
5. Нажмите **"Create repository"**

### Шаг 2: Загрузите код
```bash
# Распакуйте gigabot.zip
# Откройте командную строку в папке gigabot

git init
git add .
git commit -m "Initial commit: Gigabot system"

# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/gigabot.git
git push -u origin master
```

### Шаг 3: Разверните на Railway
1. Перейдите на [railway.app](https://railway.app)
2. **"New Project"** → **"Deploy from GitHub"**
3. Выберите репозиторий `gigabot`
4. Railway автоматически настроит проект

### Шаг 4: Настройте переменные окружения
В Railway dashboard → **"Variables"** добавьте:

```


### Шаг 5: Настройте вебхуки
1. Скопируйте URL из Railway: `https://xxxxx.railway.app`
2. В Green API настройте вебхук: `https://xxxxx.railway.app/whatsapp/webhook`

## ✅ Готово!

Теперь ваша система работает:
- WhatsApp бот принимает заказы
- Telegram бот управляет продавцами
- ИИ отвечает естественно
- Платежи проверяются автоматически

## 🔧 Локальный запуск

```bash
pip install -r requirements.txt
python run.py
```

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
