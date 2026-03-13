from supabase import create_client
from config import Settings

settings = Settings()

client = create_client(settings.supabase_url, settings.supabase_key)

# may wrap additional helpers here
