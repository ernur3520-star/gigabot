from fastapi import FastAPI

from config import Settings
from whatsapp import webhook as whatsapp_webhook

app = FastAPI(title="Gigabot Internet Packages Manager")
settings = Settings()

# register sub-routers
app.include_router(whatsapp_webhook.router)

# other routers (telegram webhook if using, admin API, etc.) can be added here

@app.get("/")
def root():
    return {"message": "Gigabot service is running"}
