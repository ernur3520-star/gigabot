# order-related handlers and helpers

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
# from database import queries

# Temporary storage for orders
orders_list = []

async def show_new_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    seller_id = update.effective_user.id
    
    # try:
    #     result = queries.get_orders_by_seller(seller_id)
    #     orders = result.data if result.data else []
    #     new_orders = [o for o in orders if o.get("status") == "new"]
    # except Exception as e:
    #     print(f"Error loading orders: {e}")
    #     new_orders = orders_list  # fallback to temp storage
    new_orders = [o for o in orders_list if o["status"] == "new"]
    
    if not new_orders:
        text = "Новых заказов нет." if lang == "ru" else "Жаңа тапсырыстар жоқ."
    else:
        text = "Новые заказы:\n\n" if lang == "ru" else "Жаңа тапсырыстар:\n\n"
        for i, order in enumerate(new_orders, 1):
            text += f"{i}. От: {order['sender']}\n{order['text']}\n\n"
        # Mark as viewed
        for o in new_orders:
            # try:
            #     queries.update_order_status(o['id'], 'viewed')
            # except Exception as e:
            #     print(f"Error updating order status: {e}")
            #     # Update in temp list if DB fails
            #     if o in orders_list:
            o["status"] = "viewed"
    
    buttons = [
        [InlineKeyboardButton("🔄 Обновить" if lang == "ru" else "🔄 Жаңарту", callback_data="menu_orders_new")],
        [InlineKeyboardButton("⬅️ Назад" if lang == "ru" else "⬅️ Артқа", callback_data="menu_back")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

async def show_all_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("language", "ru")
    seller_id = update.effective_user.id
    
    # try:
    #     result = queries.get_orders_by_seller(seller_id)
    #     orders = result.data if result.data else []
    # except Exception as e:
    #     print(f"Error loading orders: {e}")
    #     orders = orders_list  # fallback
    orders = orders_list
    
    if not orders:
        text = "Заказов нет." if lang == "ru" else "Тапсырыстар жоқ."
    else:
        text = "Все заказы:\n\n" if lang == "ru" else "Барлық тапсырыстар:\n\n"
        for i, order in enumerate(orders, 1):
            status = "Новый" if order["status"] == "new" else "Просмотрен" if lang == "ru" else "Жаңа" if order["status"] == "new" else "Қаралған"
            text += f"{i}. Статус: {status}\nОт: {order['sender']}\n{order['text']}\n\n"
    
    buttons = [
        [InlineKeyboardButton("⬅️ Назад" if lang == "ru" else "⬅️ Артқа", callback_data="menu_back")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
