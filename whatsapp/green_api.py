import requests
from config import Settings

settings = Settings()

class GreenAPI:
    def __init__(self):
        self.instance = settings.green_api_instance
        self.token = settings.green_api_token
        self.base = f"https://api.green-api.com/{self.instance}"

    def send(self, endpoint: str, data: dict):
        url = f"{self.base}/{endpoint}?token={self.token}"
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        return resp.json()

    # add other helpers as needed
