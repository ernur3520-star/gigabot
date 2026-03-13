from pydantic import BaseModel
from typing import Optional

# define data models for Supabase

class Seller(BaseModel):
    id: str
    name: str
    whatsapp_number: str
    kaspi_card: str
    packages: dict
    active: bool
    language: Optional[str]
    subscription_expires: Optional[str]

class Order(BaseModel):
    id: str
    seller_id: str
    client_whatsapp: str
    gigabytes: int
    operator: str
    status: str  # new, sent, problem, cancelled
    payment_checked: bool
    created_at: str
