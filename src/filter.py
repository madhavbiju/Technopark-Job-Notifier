import logging
import re
from typing import List
from .models import Job
from .config import Config

logger = logging.getLogger(__name__)

class JobFilter:
    def __init__(self, keywords: List[str] = None):
        self.keywords = keywords if keywords is not None else Config.KEYWORDS

    def is_match(self, job: Job) -> bool:
        if not self.keywords:
            return True  # If no keywords are configured, consider everything a match

        text_to_search = f"{job.job_title} {job.company.name}".lower()
        
        for keyword in self.keywords:
            # Escape the keyword to handle characters like '.' in 'react.js'
            # Use \b to ensure we match whole words only.
            # E.g., 'ai' won't match 'maintenance', 'retail', etc.
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_to_search):
                return True
                
        return False
