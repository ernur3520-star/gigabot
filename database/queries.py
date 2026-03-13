# helper functions to query Supabase
from supabase import create_client
from config import Settings

settings = Settings()

supabase = create_client(settings.supabase_url, settings.supabase_key)


def save_message(message_data: dict):
    # TODO: implement message saving
    pass


def insert_seller(seller_data: dict):
    return supabase.table('sellers').insert(seller_data).execute()


def get_seller_by_telegram_id(telegram_id: int):
    return supabase.table('sellers').select('*').eq('telegram_id', telegram_id).execute()


def update_seller(telegram_id: int, updates: dict):
    return supabase.table('sellers').update(updates).eq('telegram_id', telegram_id).execute()


def insert_order(order_data: dict):
    return supabase.table('orders').insert(order_data).execute()


def get_orders_by_seller(seller_id: int):
    return supabase.table('orders').select('*').eq('seller_id', seller_id).order('created_at', desc=True).execute()


def update_order_status(order_id: int, status: str):
    return supabase.table('orders').update({'status': status}).eq('id', order_id).execute()


# TODO: implement other queries: messages, etc.
