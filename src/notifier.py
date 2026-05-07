import requests
import logging
from html import escape
from typing import List
from .models import Job
from .config import Config

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self, bot_token: str = Config.TELEGRAM_BOT_TOKEN, chat_id: str = Config.TELEGRAM_CHAT_ID):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, text: str) -> bool:
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured. Skipping notification.")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def notify_jobs(self, jobs: List[Job]) -> List[Job]:
        sent_jobs = []

        if not jobs:
            return sent_jobs

        for job in jobs:
            message = self._format_job_message(job)
            success = self.send_message(message)
            if success:
                sent_jobs.append(job)
                logger.info(f"Successfully notified about job: {job.job_title} at {job.company.name}")
            else:
                logger.error(f"Notification failed for job: {job.job_title} at {job.company.name}")

        return sent_jobs

    def _format_job_message(self, job: Job) -> str:
        job_url = f"https://technopark.in/job-details/{job.job_listing_id}"
        return (
            f"🚀 <b>New Job Match Found!</b>\n\n"
            f"<b>Title:</b> {escape(job.job_title)}\n"
            f"<b>Company:</b> {escape(job.company.name)}\n"
            f"<b>Posted Date:</b> {escape(job.posted_date)}\n"
            f"<b>Closing Date:</b> {escape(job.closing_date or 'N/A')}\n\n"
            f'<a href="{escape(job_url, quote=True)}">Apply Here</a>'
        )
