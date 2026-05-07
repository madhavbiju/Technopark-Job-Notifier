import logging
import sys
from .config import Config
from .fetcher import JobFetcher
from .filter import JobFilter
from .notifier import TelegramNotifier
from .storage import Storage

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('job_search.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Technopark Job Search Script...")
    
    # Optional: validate config
    try:
        Config.validate()
    except ValueError as e:
        logger.warning(f"Config warning: {e}")
        logger.warning("Continuing without notifications if tokens are missing.")

    fetcher = JobFetcher()
    job_filter = JobFilter()
    notifier = TelegramNotifier()
    storage = Storage()
    
    new_matched_jobs = []

    try:
        for job in fetcher.get_all_jobs():
            # Check if we already notified about this job
            if storage.is_notified(job.id):
                continue
                
            # Check if it matches our keywords
            if job_filter.is_match(job):
                new_matched_jobs.append(job)
                # Mark it as notified so we don't process it again next run
                storage.mark_notified(job.id)

        if new_matched_jobs:
            logger.info(f"Found {len(new_matched_jobs)} new matching jobs. Sending notifications...")
            notifier.notify_jobs(new_matched_jobs)
        else:
            logger.info("No new matching jobs found today.")

    except Exception as e:
        logger.error(f"An unexpected error occurred during execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()
