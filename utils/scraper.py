from jolescraper import JoleScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_scraped_data(url: str, tags: list) -> str:
    try:
        scraper = JoleScraper(url, tags)
        data = scraper.request_data()
        scraped_data = scraper.process_data(data)

        return scraped_data
    except Exception as e:
        logger.error(f"Error: {e}")
        raise RuntimeError(f"An error occurred: {e}")
    
