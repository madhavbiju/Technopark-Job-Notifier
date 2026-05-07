# Technopark Job Scraper & Telegram Notifier

An automated Python tool that monitors the Technopark jobs API for new job postings matching your specific keywords, and alerts you instantly via a Telegram Bot.

## Features

- **Keyword Filtering:** Only get notified about jobs that matter to you. Uses strict word-boundary regex matching to avoid false positives.
- **Deduplication:** Uses a lightweight local SQLite database (`jobs.db`) to keep track of notified jobs.
- **GitHub Actions Ready:** Designed to be run on a schedule in the cloud. It commits the deduplication database back to the repo after successful notifications so scheduled runs maintain state.

---

## 🚀 Setup for Local Development

### 1. Clone & Setup Environment

```bash
git clone https://github.com/yourusername/technopark-job-scraper.git
cd technopark-job-scraper

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the sample environment file:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

- `TELEGRAM_BOT_TOKEN`: The token you get from [@BotFather](https://t.me/BotFather) on Telegram.
- `TELEGRAM_CHAT_ID`: Your personal Chat ID (You can get this from bots like [@userinfobot](https://t.me/userinfobot)).
- `KEYWORDS`: A comma-separated list of keywords to match (e.g., `react,nodejs,full stack`).
- `MAX_PAGES`: (Optional) The maximum number of pages to check on the API. Set to `999` to check all pages.

### 3. Run the Scraper

```bash
python run.py
```

Check your Telegram for new matches!

---

## ☁️ Running for Free on GitHub Actions

You can deploy this script to run automatically every day using GitHub Actions.

1. **Push your code** to a private or public GitHub Repository. (The `.gitignore` will ensure your `.env` and local logs stay out of git. The workflow force-adds `jobs.db` because it is the scheduled scraper's deduplication state).
2. Go to your repository **Settings** -> **Secrets and variables** -> **Actions**.
3. Under the **Secrets** tab, add:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Under the **Variables** tab, add:
   - `KEYWORDS` (e.g. `python, django, react`)
5. Go to **Settings** -> **Actions** -> **General**, scroll down to **Workflow permissions**, and select **Read and write permissions**. This is _critical_ because the action needs to save the `jobs.db` file back to the repository so you don't get duplicate notifications the next day.

Once configured, the workflow (`.github/workflows/job_scraper.yml`) will automatically run every day at 10:00 AM IST. You can also trigger it manually from the "Actions" tab.

## Architecture & Code Structure

- `run.py`: The entry point.
- `src/fetcher.py`: Connects to the API and retrieves job listings using `requests`.
- `src/filter.py`: Handles strict word-boundary matching to filter jobs based on your keywords.
- `src/storage.py`: Manages the SQLite deduplication state.
- `src/notifier.py`: Formats the alert and sends it via the Telegram API.
- `src/models.py`: Data structures (`Job`, `Company`).
