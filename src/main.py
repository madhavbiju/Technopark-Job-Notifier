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
    Config.validate()

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

        if new_matched_jobs:
            logger.info(f"Found {len(new_matched_jobs)} new matching jobs. Sending notifications...")
            notified_jobs = notifier.notify_jobs(new_matched_jobs)
            for job in notified_jobs:
                storage.mark_notified(job.id)

            failed_count = len(new_matched_jobs) - len(notified_jobs)
            if failed_count:
                raise RuntimeError(f"Failed to notify {failed_count} matched job(s).")
        else:
            logger.info("No new matching jobs found today.")

    except Exception as e:
        logger.error(f"An unexpected error occurred during execution: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
