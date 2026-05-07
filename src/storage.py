import sqlite3
import logging
from .config import Config

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self, db_path: str = Config.DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notified_jobs (
                        job_id INTEGER PRIMARY KEY,
                        notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def is_notified(self, job_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM notified_jobs WHERE job_id = ?', (job_id,))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking if job is notified: {e}")
            raise

    def mark_notified(self, job_id: int):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT OR IGNORE INTO notified_jobs (job_id) VALUES (?)', (job_id,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error marking job as notified: {e}")
            raise
