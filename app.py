import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from cities.philly.fetch_philly_rss import main as fetch_philly_rss
from sports.cbb.fetch_ncaa_rss import main as fetch_ncaa_rss
from sports.nfl.fetch_pff_rss import main as fetch_pff_rss
from sports.mlb.fetch_foxmlb_rss import main as fetch_foxmlb_rss
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)

def fetch_all_feeds():
    philly_news = fetch_philly_rss()
    cbb_news = fetch_ncaa_rss()
    pff_news = fetch_pff_rss()
    foxmlb_news = fetch_foxmlb_rss()
    if philly_news:
        logging.info(f"PHILLY news posted: {philly_news}")
    else:
        logging.info("Nothing new posted for Philly.")
    if cbb_news:
        logging.info(f"NCAA news posted: {cbb_news}")
    else:
        logging.info("Nothing new posted for NCAA.")
    if pff_news:
        logging.info(f"PFF news posted: {pff_news}")
    else:
        logging.info("Nothing new posted for PFF.")
    if foxmlb_news:
        logging.info(f"FOX MLB news posted: {foxmlb_news}")
    else:
        logging.info("Nothing new posted for FOX MLB.")


def main():
    # Create a scheduler instance
    scheduler = BlockingScheduler()

    # Schedule the job to run every 15 minutes
    scheduler.add_job(fetch_all_feeds, 'interval', minutes=15)

    try:
        # Start the scheduler
        scheduler.start()
    except KeyboardInterrupt:
        # Stop the scheduler if interrupted
        scheduler.shutdown()

if __name__ == "__main__":
    main()
