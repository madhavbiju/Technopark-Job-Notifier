import requests
import logging
from typing import List, Generator
from .models import Job
from .config import Config

logger = logging.getLogger(__name__)

class JobFetcher:
    def __init__(self):
        self.session = requests.Session()
        # Adding headers to mimic a normal browser request
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
            'Referer': 'https://technopark.in/job-search',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def fetch_page(self, page: int = 1) -> dict:
        url = f"{Config.API_URL}?page={page}&search=&type="
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page}: {e}")
            return {}

    def get_all_jobs(self) -> Generator[Job, None, None]:
        current_page = 1
        
        while current_page <= Config.MAX_PAGES:
            logger.info(f"Fetching page {current_page}...")
            data = self.fetch_page(current_page)
            
            if not data or 'data' not in data:
                break
                
            jobs_data = data['data']
            if not jobs_data:
                break
                
            for job_data in jobs_data:
                yield Job.from_dict(job_data)
                
            if current_page >= data.get('last_page', 1):
                break
                
            current_page += 1
