import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Comma-separated keywords, strip whitespace
    _keywords_raw: str = os.getenv("KEYWORDS", "")
    KEYWORDS: List[str] = [k.strip().lower() for k in _keywords_raw.split(",") if k.strip()] if _keywords_raw else []
    
    API_URL: str = os.getenv("API_URL", "https://technopark.in/api/paginated-jobs")
    MAX_PAGES: int = int(os.getenv("MAX_PAGES", "5"))
    DB_PATH: str = os.getenv("DB_PATH", "jobs.db")

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment.")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID is not set in environment.")
